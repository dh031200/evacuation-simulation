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
    # print(environment.info['entrance'])
    agent_pool = AgentPool(generate_frequency=1.0, goal=environment.info['rally_point'], adult_kids_ratio=0.7, random_move_ratio=0.1)
    _map = environment.info['map'].copy()
    # agent_pool.generate([223,433])
    # agent_pool.generate([349,314])
    # _map = environment.info['map'].copy()
    # for agent in agent_pool.pool:
    #     _next = agent.check(environment.get_area(_map, agent.location, agent.sight))
    # show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool)  # , area)
    # wait()
    # print(f"environment.info['rally_point'] : {environment.info['rally_point']}")
    for i in range(1000):
        # _map = environment.info['map'].copy()
        agent_pool.generate(environment.get_spawn_point())
        arrived = []
        for _id in agent_pool.pool:
            agent = agent_pool.pool[_id]
            # print(f'id : {_id}')
            _next = agent.check(environment.get_area(environment.info['map'], agent.location, agent.sight))
            if agent.is_arrive:
                for _loc in agent.location:
                    environment.info['map'][_loc[0], _loc[1]] = -3
                    # _map[_loc[0], _loc[1]] = -3

                arrived.append(agent.id)
                continue
            before = agent.location
            agent.move(_next)
            for b_loc, a_loc in zip(before, agent.location):
                # print(f'{b_loc} -> {a_loc}')
                # print(b_loc[0])
                # print(b_loc[1])
                # print(_map[b_loc[0],b_loc[1]])
                environment.info['map'][b_loc[0], b_loc[1]] = _map[b_loc[0],b_loc[1]]
                environment.info['map'][a_loc[0], a_loc[1]] = _id
            # print('--------------------------------------------')
            # print(agent.location)
            # print(agent.location)
            # for _loc in agent.location:
            #     print(_loc)
            #     _map[_loc[0], _loc[1]] = _id
            # for _loc in agent.location
            #     if _loc
        agent_pool.check_arrived(arrived)
        # agent_pool.process()

        show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool)  # , area)
        # wait()
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
