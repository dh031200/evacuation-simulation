# SPDX-FileCopyrightText: 2023-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == "__main__":
    from evacuation_simulation.cli import evacuation_simulation

    sys.exit(evacuation_simulation())
