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


from abc import ABC, abstractmethod
import sys


class ModuleAwareObject(ABC):

    @abstractmethod
    def bind(self, module_name: str, module):
        pass


def bind(module_name):
    module = sys.modules[module_name]
    new    = {}
    for name, obj in module.__dict__.items():
        if issubclass(type(obj), ModuleAwareObject):
            new[name] = obj.bind(module_name, module)
    for name, obj in new.items():
        module.__dict__[name] = new[name]
