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

"""greenland-debug --- Execute greenland application with debug parameters set.

Usage:
  greenland-debug \n\
    [-d ...] \n\
    [-p PROFILE] \n\
    [-D EVENTSPEC ...] \n\
    [-A EVENTSPEC ...] \n\
    [-l LOGLEVEL] [-L LOGFILE] [-F LOGFMT] \n\
    [-k TARGETKEY] \n\
    CMD [ARGS ...]
  greenland-debug [-d ...] CMD [ARGS ...]

Options:

  -l LOGLEVEL  -- Set loglevel to LOGLEVEL.
  -L LOGFILE   -- Redirect logging to LOGFILE.
  -F LOGFMT    -- Set log format to LOGFMT.

  Note, that with these options logging can only be changed globally
  (applying to all modules, i.e. the root logger). If one needs to
  redirect messages from only a specific module, increase the loglevel
  from only a specific module or ignore messages from a specific
  module, then the PROFILE parameter (-p) must be used.

  -D EVENTSPEC  -- Drop to debugger on event as specified by EVENTSPEC.

     In the most simple form, EVENTSPEC is the name of a runtime event
     (start, uncaught, debug, info, warn, error, panic). The runtime
     will drop into the debugger when one of the specified events
     occurs.

     With ">" and "~" conditions can be added to the events, so that
     the runtime only drops to the debugger if an event occurs that
     matches the condition. Example:

     - 'error>foo.bar' only drops to the debugger if the error
       originates from module foo.bar.

     - 'error~division by zero' only drops to the debugger if the
       error message matches "division by zero" as a regular
       expression.

     - 'error>foo.bar~error~division by zero' combines both
       conditions.

  -A EVENTSPEC  -- Abort on event as specified by EVENTSPEC.

  -p PROFILE  -- Use PROFILE as logging profile.

     This sets the environment variable GREENLAND_LOG_PROFILE.

  -d  -- Default debugging setup.

     Setup typical default debug parameters: Drop to debugger on
     UNCAUGHT events. This is a shortcut for -D uncaught.

     Repeat twice to also drop to debugger on ERROR events. This is a
     shortcut for -D start.

  -k TARGETKEY  -- Set target program key.

     TARGETKEY is the prefix for the environment variables. E.g. with
     '-k DEMO -p debug' the variable DEMO_DEBUG_PROFILE will be set.

     If not given, the TARGETKEY will be determined from the program:

     - foo/bar.py => TARGETKEY is 'BAR'
     - bar        => TARGETKEY is 'BAR'
     - foo/bar    => TARGETKEY is 'GREENLAND'.

     The implicit assumption in the latter case is, that bar is a
     script that calls one or more python programs.

Parameters:

  CMD   -- The command to execute.

           If CMD contains a directory path, then it will be assumed
           to be a python source file and be executed with the python
           interpreter. If it's a name without a directory path, it
           will be assumed to be on the search PATH and be directly
           executable. Invoking python will be ommitted.

  ARGS  -- The arguments to pass to CMD.

"""


from docopt import docopt
from .. import version as versions  # noqa
from ..program_info import program
from ..logging import per_module    # noqa, injection
from ..logging import debug         # noqa
from ..start import run

from ..app import greenland_debug

from .. import module_aware_objects as mao
mao.bind(__name__)


@run
def main():
    args = docopt(
        __doc__,
        version = program.descriptive_string,
        options_first = True
    )
    if debug:
        debug(f"args = {args}")

    greenland_debug.main(
        loglevel        = args['-l'],
        logfile         = args['-L'],

        logformat       = args['-F'],

        break_events    = args['-D'],
        abort_events    = args['-A'],

        profile         = args['-p'],
        debuglevel      = args['-d'],

        command = [args['CMD']] + args['ARGS'],

        target = args['-k']
    )
