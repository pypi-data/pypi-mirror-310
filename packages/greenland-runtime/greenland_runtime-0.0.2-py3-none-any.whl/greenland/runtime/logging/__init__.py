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


import logging

from .base import \
    debug, info, warn, error, panic, errors, check_errors  # noqa
#
#   Note: 'noqa' because just imported for re-export

default_loglevel = logging.WARN

formats = {
    'default': "{levelname[0]} {asctime} {program_name}: {name}: {message}",
    'simple1': "{levelname[0]} {name}: {message}",
    'simple2': "{levelname[0]} {program_name}: {message}",
    'minimal': "{levelname[0]} {message}",
    'extended': ("{levelname[0]} {asctime} {program_pid}@{program_host}"
                 " {program_name}: {name}: {message}"),
}

default_format  = formats['default']
