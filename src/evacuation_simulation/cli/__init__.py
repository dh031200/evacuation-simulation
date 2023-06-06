# SPDX-FileCopyrightText: 2023-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT
import click

from evacuation_simulation.__about__ import __version__
from evacuation_simulation import Agent, AgentPool, Environment, show, wait, destroy, writer, plot, to_csv, counts


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="Evacuation-Simulation")
@click.option('--map_dir', '-m', required=True, help='map directory')
@click.option('--floor', '-f', required=True, help='floor for simulation')
@click.option('--scenario', '-s', required=True, help='scenario for simulation')
def evacuation_simulation(map_dir, floor, scenario):
    click.echo("Hello world!")
    environment = Environment(map_dir, floor, scenario)
    # print(environment.info['entrance'])
    agent_pool = AgentPool(generate_frequency=0.7, goal=environment.info['rally_point'], adult_kids_ratio=0.7,
                           random_move_ratio=0.1)
    _map = environment.info['map'].copy()
    video_writer = writer(environment.height, environment.width)
    occupancy_rate = []
    verbose = []
    num_activate_agents = []
    num_total_agents = []
    # agent_pool.generate([223,433])
    # agent_pool.generate([297, 179])
    # _map = environment.info['map'].copy()
    # for agent in agent_pool.pool:
    #     _next = agent.check(environment.get_area(_map, agent.location, agent.sight))
    # show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool)  # , area)
    show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool, video_writer)
    # env_dict = counts(v_map)
    #
    # total = env_dict[(255,255,255)] + env_dict[(255,0,0)]
    # wait()

    # print(f"environment.info['rally_point'] : {environment.info['rally_point']}")
    for i in range(10000):
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
                environment.info['map'][b_loc[0], b_loc[1]] = _map[b_loc[0], b_loc[1]]
                environment.info['map'][a_loc[0], a_loc[1]] = _id

        agent_pool.check_arrived(arrived)

        show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool, video_writer)  # , area)

        if not i % 150:
            num_activate_agents.append(len(agent_pool))
            num_total_agents.append(agent_pool.get_id()-1)
            occupancy_rate.append(round(environment.calc_occupancy() / environment.movable * 100, 4))
            verbose.append(i)

            plot(num_activate_agents, num_total_agents, occupancy_rate, verbose)
            to_csv(num_activate_agents, num_total_agents, occupancy_rate, verbose)

            # env_dict = counts(v_map)
            # current = env_dict[(0,0,255)] + env_dict[(255,0,0)]
            #
            # print(f'{current} / {total}')
            # print(round(current / total * 100, 4))

        # wait()
    destroy()
    video_writer.release()

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


# total
# 320988

