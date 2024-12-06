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

from . import logging as _logging
from .logging import info
from .program_info import program
from .events import raise_event, START, UNCAUGHT
from typing import Callable, Union

import sys
from sys import modules

import greenland.runtime.module_aware_objects as mao
mao.bind(__name__)

_previous_handler: Union[Callable, None]


def _uncaught_handler(type, value, traceback):

    global _previous_handler

    raise_event(
        UNCAUGHT,
        '__main__',                       # origin is fake, intentionally
        f"Uncaught {type}: {value}",
        type = type,
        value = value,
        traceback = traceback
    )
    if _previous_handler is not None:
        return _previous_handler(type, value, traceback)
    else:
        return


def _start(main):

    global _previous_handler

    version = program.version
    raise_event(
        START,
        '__main__',                       # origin is fake, intentionally
        f"Starting {repr(program.name)},"
        f" version {version}",
        program = program.name,
        version = version
    )
    if info:
        info(
            f"Program {repr(program.name)},"
            f" version {program.version}"
        )

    _previous_handler = sys.excepthook
    sys.excepthook = _uncaught_handler

    main()
    _logging.check_errors()

    # TODO: Add some drop-to-debugger functionality here.
    #       - Drop to debugger before start if flags ar set
    #       - Set uncaught exception handler
    #
    #       All dependent on configuration (per envvar)


def run(main, start_name = 'start'):
    name   = main.__module__
    module = modules[name]
    module.__dict__[main.__name__] = main  # [1]
    wrapper  = module.__dict__[start_name] = (lambda: _start(main))
    if name == '__main__':
        wrapper()
    return main

# [1]: To ensure the main is bound to it's name in the module before
#      we run it from the decorator. The peculiarity of this approach
#      is, that main is run while __main__ is loaded, but this means
#      it needs to be the last statement in __main__.
