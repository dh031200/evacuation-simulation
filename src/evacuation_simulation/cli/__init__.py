# SPDX-FileCopyrightText: 2023-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT
import click

from evacuation_simulation.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="Evacuation-Simulation")
def evacuation_simulation():
    click.echo("Hello world!")
