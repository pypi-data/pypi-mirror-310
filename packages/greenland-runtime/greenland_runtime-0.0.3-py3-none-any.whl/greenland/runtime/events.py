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

from greenland.base.enums import Enum
from .control import Panic
from typing import Callable
from abc import ABC
from . import env_vars

import pdb
import sys
import re


class Abort(Panic):
    pass


class EventType(Enum):
    pass


UNCAUGHT = EventType('UNCAUGHT')
START    = EventType('START')
USER     = EventType('USER')

DEBUG = EventType('DEBUG')
INFO  = EventType('INFO')
WARN  = EventType('WARN')
ERROR = EventType('ERROR')
PANIC = EventType('PANIC')


EventType.finalize()


def always(origin: str, message: str, *pargs, **kwargs):
    return True


class HandlingOracle(ABC):

    def should_drop_into_debugger(
            self,
            event_type, origin: str, message: str, *pargs, **kwargs
    ):
        return False

    def should_abort(
            self,
            event_type, origin: str, message: str, *pargs, **kwargs
    ):
        return False

    def handle_event(
            self, event_type, origin: str, message: str, *pargs, **kwargs
    ):
        if self.should_drop_into_debugger(
                event_type, origin, message, *pargs, **kwargs
        ):
            print(
                f"\n*** Dropping into debugger on {event_type} {message!r}"
                f" from {origin} with {pargs}, {kwargs}.",
                file = sys.stderr
            )
            if event_type != UNCAUGHT:
                print(file = sys.stderr)
                pdb.set_trace()
            else:
                print(
                    "*** Invoking postmortem debugging.\n",
                    file = sys.stderr
                )
                pdb.pm()

        if self.should_abort(
                event_type, origin, message, *pargs, **kwargs
        ):
            raise Abort(message)


class DefaultHandlingOracle(HandlingOracle):

    _debugger_conditions: dict[EventType, list[Callable]] = {
    }

    _abort_conditions: dict[EventType, list[Callable]] = {
    }

    stanza_rx = re.compile("^([a-zA-Z]+)(>([a-zA-Z0-9._]+)){0,1}(~(.*)){0,1}$")

    def __init__(self):

        self.interpret_config("DEBUGGER", self._debugger_conditions)
        self.interpret_config("ABORT", self._abort_conditions)

    def interpret_config(self, envvar_name, conditions_dict):
        config = env_vars.get_my_envvar(envvar_name)
        if config is None:
            return

        for stanza in config.split(":"):
            if len(stanza) == 0:
                continue
            m = self.stanza_rx.match(stanza)
            if not m:
                print(
                    f"Cannot interpret config stanza from *_{envvar_name}:"
                    f" {stanza!r}",
                    file = sys.stderr
                )
                continue
            self.add_condition(
                conditions_dict,
                EventType(m.group(1).upper()),
                self.compile_predicate(
                    m.group(3),
                    m.group(5)
                )
            )

    def compile_predicate(self, origin, message_rx):

        if origin is None:
            if message_rx is None:
                return always
            else:
                def make_predicate_message(message_rx):
                    rx = re.compile(message_rx, re.IGNORECASE)
                    return (
                        lambda _, message, *pargs, **kwargs:
                        rx.search(message)
                    )
                return make_predicate_message(message_rx)
        else:
            if message_rx is None:
                def make_predicate_origin(module_name):
                    return (
                        lambda origin, _, *pargs, **kwargs:
                        origin == module_name
                    )
                return make_predicate_origin(origin)
            else:
                def make_predicate_both(restricted_to_origin, message_rx):
                    rx = re.compile(message_rx, re.IGNORECASE)
                    return (
                        lambda origin, message, *pargs, **kwargs:
                        origin == restricted_to_origin
                        and rx.search(message)
                    )
                return make_predicate_both(origin, message_rx)

    def add_condition(self, conditions_dict, event_type, predicate):
        if event_type not in conditions_dict:
            conditions_dict[event_type] = []
        conditions_dict[event_type].append(predicate)

    def add_debugger_condition(self, event_type, predicate):
        self.add_condition(
            self._debugger_conditions, event_type, predicate
        )

    def add_abort_condition(self, event_type, predicate):
        self.add_condition(
            self._abort_conditions, event_type, predicate
        )

    def should_act(
            self,
            conditions,
            event_type, origin: str, message: str, *pargs, **kwargs
    ):
        try:
            predicates = conditions[event_type]
        except KeyError:
            return False

        for p in predicates:
            if p(origin, message, *pargs, **kwargs):
                return True

        return False

    def should_drop_into_debugger(
            self,
            event_type, origin: str, message: str, *pargs, **kwargs
    ):
        return self.should_act(
            self._debugger_conditions,
            event_type, origin, message, *pargs, **kwargs
        )

    def should_abort(
            self,
            event_type, origin: str, message: str, *pargs, **kwargs
    ):
        return self.should_act(
            self._abort_conditions,
            event_type, origin, message, *pargs, **kwargs
        )


oracle = DefaultHandlingOracle()


def raise_event(event_type, origin: str, message: str, *pargs, **kwargs):
    oracle.handle_event(
        event_type, origin, message, *pargs, **kwargs
    )
