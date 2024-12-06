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

from pathlib import Path
from sys import argv, modules
from os import getenv, getpid
from typing import Union


class _ProgramInfo:

    # TODO: make this into a dynamically scoped object in order to be
    # able to overwrite this for testing purposes. Low prio.

    name:    str
    path:    Path
    main:    Path

    host: Union[str, None]
    user: Union[str, None]
    pid:  int

    def __init__(self):

        self.main = Path(modules['__main__'].__file__)

        path = self.path = Path(argv[0])
        self.name = path.stem

        self.host = getenv("HOSTNAME")
        self.user = getenv("USER")

        self.pid  = getpid()

    @property
    def version(self) -> Union[str, None]:
        try:
            versions = modules['__main__'].__dict__['versions']
        except KeyError:
            versions = None

        if versions is None:
            return None
        else:
            return versions.version

    @property
    def envvar_prefix(self):
        return self.name.upper().replace("-", "_").replace(".", "_")

    @property
    def descriptive_string(self):
        return f"{self.name} {self.version}"


program = _ProgramInfo()
