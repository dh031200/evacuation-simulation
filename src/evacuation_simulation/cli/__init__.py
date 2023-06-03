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
@click.option('--scenario', '-s', required=True, help='scenario for simulation')
def evacuation_simulation(map_dir, floor, scenario):
    click.echo("Hello world!")
    environment = Environment(map_dir, floor, scenario)
    agent_pool = AgentPool(generate_frequency=0.1, adult_kids_ratio=0.7)

    for i in range(100):
        agent_pool.generate(environment.get_spawn_point())

        for agent in agent_pool.pool:
            _next = agent.check(environment.get_area(agent.location, agent.sight))

            print(agent.location)
            agent.move(_next, environment.info['rally_point'])

        show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool)  # , area)
        wait()
    destroy()

# direction = (
#     (-1, 0),  # up
#     (0, 1),  # right
#     (1, 0),  # down
#     (0, -1),  # left
# )
# print()
# print(f'dy, dx :  {dy}, {dx}')
# print(f'min_y : {min_y}')
# print(f'max_y : {max_y}')
# print(f'min_x : {min_x}')
# print(f'max_x : {max_x}')
# print(f'area[min_y:max_y, min_x:max_x] : {area[min_y:max_y, min_x:max_x]}')

# if -1 in area[min_y:max_y, min_x:max_x]:
#     print(dy,dx,'fail')

# ay, ax = y, x
# is_pass = True
# for i in range(sight):
#     ay += dy
#     ax += dx
#     # if area[]

# print(area.shape)

# a, b, c, d = y - sight, y + sight, x - sight, x + sight
# return a, b, c, d

# agent_pool = AgentPool(
#     floor=environment.floor, generate_frequency=0.1, adult_kids_ratio=0.7, check_function=environment.check
# )
# for floor in environment.floor:
#     agent_pool.generate(floor, environment.get_spawn_point(floor))
#
# for floor in environment.floor:
#     show(f'Simulation of {floor}F', environment.map[floor]['map'], agent_pool.pool)
#     wait()
#
# while True:
#     for floor in environment.floor:
#         agent_pool.move(floor)
#         agent_pool.generate(floor, environment.get_spawn_point(floor))
#         show(f'Simulation of {floor}F', environment.map[floor]['map'], agent_pool.pool)
#         wait()
