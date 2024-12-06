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
from greenland.runtime.module_aware_objects import ModuleAwareObject
from greenland.runtime.control import Panic as _Panic, errors
from greenland.runtime.program_info import program

import sys
from types import ModuleType


class Log(ModuleAwareObject):

    module_name: str
    module:      ModuleType

    def __init__(self, module_name = None, module = None):

        self.module = module
        self.module_name = module_name

    def __bool__(self):
        return False

    def __call__(self, message, *pargs, **kwargs):
        pass

    def bind(self, module_name, module):
        return self.__class__(module_name, module)

    @property
    def indicator(self):
        return self.__class__.__name__[0]

    @property
    def origin(self):
        return self.module_name

    def _print(self, message, pargs, kwargs):
        print(f"{program.name}:",
              self.indicator,
              f"{self.origin}:",
              message,
              end = "", file = sys.stderr)
        if pargs or kwargs:
            print(": ", end = "", file = sys.stderr)
            if pargs:
                print("pargs = ", pargs, end = "", file = sys.stderr)
            if kwargs:
                print("kwargs = ", kwargs, end = "", file = sys.stderr)
        print(".", file = sys.stderr)


class Debug(Log):
    pass


class Info(Log):
    pass


class Warn(Log):
    def __bool__(self):
        return True

    def __call__(self, message, *pargs, **kwargs):
        self._print(message, pargs, kwargs)


class Error(Log):

    def __bool__(self):
        return True

    def __call__(self, message, *pargs, **kwargs):
        global errors
        self._print(message, pargs, kwargs)
        errors.inc()


class Panic(Log):

    def __call__(self, message, *pargs, **kwargs):
        self._print(message, pargs, kwargs)
        print(file = sys.stderr)
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
        panic("Errors occcured, see above")
