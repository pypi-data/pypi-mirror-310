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

from ..logging import debug, info, panic
import os
import subprocess

from .. import module_aware_objects as mao
mao.bind(__name__)

HOME = os.getenv("HOME")

search_path = \
    os.getenv("GREENLAND_LOG_PROFILE_PATH") \
    or [".", ".debug", f"${HOME}/.config/greenland", f"${HOME}/.greenland"]


def main(
        command,

        loglevel  = 'DEBUG',
        logfile   = None,
        logformat = None,

        break_events = [],
        abort_events = [],
        profile      = None,
        debuglevel   = 0,

        target = None
):

    env = dict(os.environ)

    def varname(suffix):
        return f"{target}_{suffix}"

    def setvar(suffix, value):
        name = varname(suffix)
        env[name] = value
        if debug:
            debug(f"{name} = {value!r}")

    if debuglevel > 0:
        if 'uncaught' not in break_events:
            break_events.append('uncaught')
        if logformat is None:
            logformat = "simple2"

    if debuglevel > 1:
        if 'start' not in break_events:
            break_events.append('uncaught')

    if target is None:
        if len(command[0]) >= 3 and command[0][-3:] == ".py":
            target = os.path.basename(command[0][:-3])
        else:
            target = os.path.basename(command[0])

    target = target.upper()

    if debug:
        debug(f"target key = {target}")

    if logfile:
        setvar("LOG_FILE", logfile)

    if loglevel:
        # TODO: Check if level is in given set.
        setvar("LOG_LEVEL", loglevel)

    if logformat:
        setvar("LOG_FORMAT", logformat)

    if break_events:
        setvar("DEBUGGER", ":".join(break_events))

    if abort_events:
        setvar("ABORT", ":".join(abort_events))

    if profile:
        found = None
        if not os.path.exists(profile):
            for p in search_path:
                for candidate in [
                        # os.path.join(p, profile),
                        os.path.join(p, f"{profile}.log.yaml")
                ]:
                    if os.path.exists(candidate):
                        found = candidate
                        break
                if found:
                    break
            if not found:
                panic(
                    f"No profile {profile!r} found in '.' and {search_path}."
                )
            profile = found

        setvar("LOG_PROFILE", profile)

    if info:
        info(f"Command is: {command}")

    subprocess.run(command, check = True, env = env)
