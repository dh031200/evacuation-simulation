# SPDX-FileCopyrightText: 2023-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT
import click

from evacuation_simulation.__about__ import __version__
from evacuation_simulation import Agent, AgentPool, Environment, show, wait, destroy


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="Evacuation-Simulation")
@click.option('--map_dir', '-m', required=True, help='map directory')
@click.option('--floor', '-f', required=True, help='floor for simulation')
def evacuation_simulation(map_dir, floor):
    click.echo("Hello world!")
    environment = Environment(map_dir, floor)
    agent_pool = AgentPool(floor=environment.floor, generate_frequency=0.1, adult_kids_ratio=0.7,
                           check_function=environment.check)
    for floor in environment.floor:
        agent_pool.generate(floor, environment.get_spawn_point(floor))

    for floor in environment.floor:
        show(f'Simulation of {floor}F', environment.map[floor]['map'], agent_pool.pool)
        wait()

    while True:
        for floor in environment.floor:
            agent_pool.move(floor)
            agent_pool.generate(floor, environment.get_spawn_point(floor))
            show(f'Simulation of {floor}F', environment.map[floor]['map'], agent_pool.pool)
            wait()

    destroy()
