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

import pytest
import os
import subprocess
from subprocess import PIPE
from pathlib import Path


@pytest.fixture
def mypath():
    return Path(os.path.dirname(__file__))


loglevel_scenarios = [

    # label, args, demo_args, return_code, expected_log

    # TODO: eliminate expected_start

    ('defaults', [], [], 0,
     [
        '__main__: Some warning.',
         '__main__: Some error.',
     ]),
    ('panic', [], ['-p'], 1,
     [
        '__main__: Some warning.',
         '__main__: Some error.',
         '__main__: Some panic.',
         '__main__: *** RAISING PANIC NOW ***.',
     ]),
    ('loglevel-error', ['-l', 'error'], [], 0,
     [
         '__main__: Some error.',
     ]),
    ('loglevel-warning', ['-l', 'warning'], [], 0,
     [
         '__main__: Some warning.',
         '__main__: Some error.',
     ]),
    ('loglevel-info', ['-l', 'info'], [], 0,
     [
         '__main__: Some info message.',
         '__main__: Some warning.',
         '__main__: Some error.',
     ]),

    ('loglevel-debug', ['-l', 'debug'], [], 0,
     [
         '__main__: Some info message.',
         '__main__: Some debug message.',
         '__main__: Some warning.',
         '__main__: Some error.',
     ]),
]


@pytest.mark.parametrize(
    "args, demo_args, return_code, expected_log",
    [s[1:] for s in loglevel_scenarios],
    ids = [s[0] for s in loglevel_scenarios],
)
def test_loglevel(mypath, args, demo_args, return_code, expected_log):
    result = subprocess.run(
        ['greenland-debug', *args, mypath / "demo.py", *demo_args],
        stderr = PIPE,
        encoding = 'utf-8'
    )

    raw_lines = result.stderr.split("\n")
    start = raw_lines.index("*** START TEST OUTPUT ***")
    lines = []
    try:
        stop  = raw_lines.index("Traceback (most recent call last):")
    except ValueError:
        stop = -1

    for line in raw_lines[start+1:stop]:
        line = " ".join(line.split()[4:])
        if line:
            lines.append(line)

    assert result.returncode == return_code
    assert lines == expected_log
