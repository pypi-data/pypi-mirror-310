#!/usr/bin/env python3
#
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

"""test_base_logging/demo.py

Usage:
  demo.py [-p] [-e]

Options:
  -h --help   Show this screen.
  -p          Panic instead of exit()
  -e          Don't suppress error checks.
"""

import greenland.runtime.version as versions  # noqa: This is only for start
import greenland.runtime.logging.per_module   # noqa: Dep injection

from greenland.runtime.logging import \
    debug, info, warn, error, panic, errors, check_errors  # noqa: re-export

# Note: Alternatively one might directly import from per_module

from greenland.runtime.start import run

import sys
from docopt import docopt

import greenland.runtime.module_aware_objects as mao
mao.bind(__name__)


@run
def main():

    if __name__ == '__main__':
        args = docopt(__doc__, version='demo.py')

    if info:
        info(f"sys.version_info = {sys.version_info!r}")

    print("*** START TEST OUTPUT ***", file=sys.stderr)

    if info:
        info("Some info message")

    if debug:
        debug("Some debug message")  # Will not turn up with base.py

    if warn:
        warn("Some warning")

    if error:
        error("Some error")

    if args['-p']:
        panic("Some panic")
    else:
        if not args['-e']:
            exit(0)
