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

import greenland.runtime.version as versions # noqa: This is only for start
import greenland.runtime.logging.per_module  # noqa: Dep injection

from greenland.runtime.logging import \
    debug, info, warn, error, panic, errors, check_errors # noqa: for re-export

# Note: Alternatively one might directly import from per_module

from greenland.runtime.start import run

import greenland.runtime.module_aware_objects as mao
mao.bind(__name__)


@run
def main():

    if debug:
        print("Debug is armed")
        debug("Some debug message")  # Will not turn up with base.py

    if warn:
        warn("Some warning")

    if error:
        error("Some error")

    panic("Just some panic")
