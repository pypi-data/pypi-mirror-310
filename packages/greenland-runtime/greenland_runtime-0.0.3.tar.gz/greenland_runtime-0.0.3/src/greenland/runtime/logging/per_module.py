# greenland-runtime -- Common runtime for greenland programs.
# Copyright (C) 2024
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import greenland.runtime.module_aware_objects as mao
from greenland.runtime.logging.base import Log as _LogBase
import greenland.runtime.logging
from greenland.runtime.control import Panic as _Panic, errors
from .. import events
from ..events import raise_event
from ..program_info import program
from .. import env_vars
import sys
import logging
from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path


class _LoggingConfigurator(ABC):

    @abstractmethod
    def loglevel(self, name):
        pass

    @abstractmethod
    def propagate(self, name) -> bool:
        pass

    @abstractmethod
    def capture_file(self, name) -> Union[str, None]:
        pass

    @abstractmethod
    def format(self, name):
        pass

    def configure_all_loggers(self):
        pass


class _SimpleConfigurator(_LoggingConfigurator):

    _loglevel: int
    _logfile:  str
    _format:   str

    def __init__(self):

        symbolic = env_vars.get_my_envvar("LOG_LEVEL")
        if symbolic is None:
            self._loglevel = greenland.runtime.logging.default_loglevel
        else:
            self._loglevel = logging.getLevelName(symbolic)

        self._logfile = env_vars.get_my_envvar("LOG_FILE")

        self._format = self.resolve_format(
            env_vars.get_my_envvar("LOG_FORMAT")
        )

    def resolve_format(self, format):
        try:
            return greenland.runtime.logging.formats[format]
        except KeyError:
            if format is not None:
                return format
            else:
                return greenland.runtime.logging.default_format

    def loglevel(self, name) -> Union[int, None]:
        if name == '':
            return self._loglevel
        else:
            return None

    def propagate(self, name) -> bool:
        return True

    def capture_file(self, name) -> Union[str, None]:
        if name == '':
            return self._logfile
        else:
            return None

    def format(self, name):
        if name == '':
            return self._format
        else:
            return None


class _FromFileConfigurator(_SimpleConfigurator):

    # TODO: Need to configure loggers for every module in the file, too

    _data: dict

    def __init__(self, filename):
        super().__init__()
        try:
            format, name = filename.split(':')
        except ValueError:
            name   = filename
            format = None

        filename = Path(name)

        if format is None:
            format = filename.suffix
            if format == '':
                format = 'yaml'
            else:
                format = format[1:]

        with open(filename, encoding = 'utf-8') as strm:
            if format == 'yaml':
                import yaml
                self._data = yaml.safe_load(strm)
            else:
                assert format == 'json'
                import json
                self._data = json.load(strm)

    def get_value(self, conversion, *keys, default = None):

        data = self._data
        for key in keys:
            if data is None:
                return default
            if key in data:
                data = data[key]
            else:
                return default

        return conversion(data)

    def loglevel(self, name):
        if name == '':
            return (
                self.get_value(logging.getLevelName, 'loglevel')
                or super().loglevel(name)
            )
        else:
            return self.get_value(
                logging.getLevelName, 'modules', name, 'loglevel'
            )

    def propagate(self, name) -> bool:
        if name == '':
            return self.get_value(
                bool, 'propagate', default = False
            )
        else:
            return self.get_value(
                bool,
                'modules', name, 'propagate',
                default = True
            )

    def capture_file(self, name) -> Union[str, None]:
        if name == '':
            return (
                self.get_value(str, 'logfile')
                or super().capture_file(name)
            )
        else:
            return self.get_value(
                str,
                'modules', name, 'logfile',
            )

    def parent_format(self, name):
        if name != '':
            try:
                parent_name = name[0:name.rindex(".")]
            except ValueError:
                parent_name = ''
            return self.format(parent_name)
        else:
            return self._format

    def format(self, name):
        if name == '':
            return (
                self.get_value(self.resolve_format, 'format')
                or super().format(name)
            )
        else:
            return (
                self.get_value(self.resolve_format, 'modules', name, 'format')
                or self.parent_format(name)
            )

    def configure_all_loggers(self):
        modules = self.get_value(
            (lambda x: x),
            'modules'
        )

        if modules is not None:
            for name in modules:
                _PerModuleLogControl.get(name)


_profile = env_vars.get_my_envvar("LOG_PROFILE")


if _profile is None:
    configurator = _SimpleConfigurator()
else:
    configurator = _FromFileConfigurator(_profile)


logging.basicConfig(
    style  = '{',
    level  = configurator.loglevel(''),
    format = configurator.format('')
)


extra_info = {
    'program_name':    program.name,
    'program_pid':     program.pid,
    'program_host':    program.host,
    'program_user':    program.user
}


class _PerModuleLogControl:

    module_name: str
    controls:    dict[str, '_PerModuleLogControl'] = {}
    level:       int
    parent:      '_PerModuleLogControl'

    def __init__(self, module_name):

        if module_name != '':
            try:
                parent_name = module_name[0:module_name.rindex(".")]
            except ValueError:
                parent_name = ''
            self.parent = self.get(parent_name)
        else:
            self.parent = None

        self.module_name = module_name

        level  = configurator.loglevel(module_name)
        logger = self.logger = logging.getLogger(module_name)

        if level is None:
            self.level = self.logger.getEffectiveLevel()
        else:
            self.level = level
            logger.setLevel(level)

        logger.propagate = configurator.propagate(module_name)

        capture_file = configurator.capture_file(module_name)

        if capture_file is not None:
            for handler in list(logger.handlers):
                logger.removeHandler(handler)
            handler = logging.FileHandler(capture_file)
            handler.setFormatter(logging.Formatter(
                style = '{',
                fmt   = configurator.format(module_name)
            ))
            logger.addHandler(handler)

            if logging.INFO >= self.level:
                logger.log(
                    logging.INFO,
                    f"Opened logfile {capture_file!r}",
                    extra = extra_info
                )

        if logging.DEBUG >= self.level:
            logger.log(
                logging.DEBUG,
                f"Logging/loading {module_name!r};"
                f" loglevel={logging.getLevelName(self.level)}",
                extra = extra_info
            )

    @classmethod
    def get(cls, module_name):
        # TODO: Lock
        if module_name not in cls.controls:
            cls.controls[module_name] = cls(module_name)
        return cls.controls[module_name]


class _Log(_LogBase):

    control: _PerModuleLogControl
    logger:  logging.Logger
    level:   int

    def __init__(self, module_name = None, module = None):
        super().__init__(module_name, module)
        if module_name is not None:
            control = self.control = _PerModuleLogControl.get(module_name)
            self.logger  = control.logger

    def __bool__(self):
        return self.level >= self.control.level

    def __call__(self, message, *pargs, **kwargs):

        # TODO: Handle pargs, kwargs => log or print as auxiliary information.

        self.logger.log(
            self.level, f"{message}.",
            extra = extra_info
        )
        if self.event_type is not None:
            raise_event(
                self.event_type, self.module_name, message, *pargs, **kwargs
            )


class Debug(_Log):
    level      = logging.DEBUG
    event_type = events.DEBUG


class Info(_Log):
    level      = logging.INFO
    event_type = events.INFO


class Warn(_Log):
    level      = logging.WARNING
    event_type = events.WARN


class Error(_Log):
    level      = logging.ERROR
    event_type = events.ERROR

    def __call__(self, message, *pargs, **kwargs):
        # TODO: Handle pargs, kwargs
        errors.inc()
        super().__call__(message, *pargs, **kwargs)


class Panic(_Log):
    level      = logging.CRITICAL
    event_type = events.PANIC

    def __call__(self, message, *pargs, **kwargs):
        # TODO: Handle pargs, kwargs
        super().__call__(message, *pargs, **kwargs)
        super().__call__("*** RAISING PANIC NOW ***")
        print("", file=sys.stderr)
        raise _Panic(message)


panic = Panic()

mao.bind(__name__)

# Note: We only want to bin panic(), but we need to bind it, to get
# proper origin (module) info with check_errors which calls panic()

debug = Debug()
info  = Info()
warn  = Warn()
error = Error()


def check_errors():
    if errors:
        panic("check_errors: Errors occcured, see above")


# injecting implementations

_target = greenland.runtime.logging.__dict__
_source = sys.modules[__name__].__dict__

for _name in _target.keys():
    if _name[0] == '_':
        continue
    if _name in _source:
        _target[_name] = _source[_name]


configurator.configure_all_loggers()
