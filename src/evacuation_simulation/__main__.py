# SPDX-FileCopyrightText: 2023-present Danny Kim <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == "__main__":
    from evacuation_simulation.cli import evacuation_simulation

    sys.exit(evacuation_simulation())
