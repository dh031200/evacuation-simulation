# SPDX-FileCopyrightText: 2023-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT
import click

from evacuation_simulation.__about__ import __version__

from evacuation_simulation import Agent, Environment, show, wait, destroy


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="Evacuation-Simulation")
def evacuation_simulation():
    click.echo("Hello world!")
    agent = Agent([0, 0])
    environment = Environment()
    print(agent.location)
    print(environment)
    show('2nd', environment.map['2nd'])
    wait()

    show('3rd', environment.map['3rd'])
    wait()

    destroy()
