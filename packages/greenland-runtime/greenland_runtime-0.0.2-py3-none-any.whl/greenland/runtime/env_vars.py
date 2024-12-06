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

from .program_info import program
from typing import Union
from os import getenv


def envvar_names(suffix):
    for prefix in (program.envvar_prefix, 'GREENLAND'):
        yield f"{prefix}_{suffix}"


def get_my_envvar(suffix) -> Union[str, None]:
    for name in envvar_names(suffix):
        val = getenv(name)
        if val is not None:
            return val
    return None
