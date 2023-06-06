# SPDX-FileCopyrightText: 2023-present Danny Kim <imbird0312@gmail.com>
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
    agent_pool = AgentPool(generate_frequency=0.7, goal=environment.info['rally_point'], adult_kids_ratio=0.7,
                           random_move_ratio=0.1)
    _map = environment.info['map'].copy()
    video_writer = writer(environment.height, environment.width)
    occupancy_rate = []
    verbose = []
    num_activate_agents = []
    num_total_agents = []
    show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool, video_writer)

    for i in range(10000):
        agent_pool.generate(environment.get_spawn_point())
        arrived = []
        for _id in agent_pool.pool:
            agent = agent_pool.pool[_id]
            _next = agent.check(environment.get_area(environment.info['map'], agent.location, agent.sight))
            if agent.is_arrive:
                for _loc in agent.location:
                    environment.info['map'][_loc[0], _loc[1]] = -3

                arrived.append(agent.id)
                continue
            before = agent.location
            agent.move(_next)
            for b_loc, a_loc in zip(before, agent.location):
                environment.info['map'][b_loc[0], b_loc[1]] = _map[b_loc[0], b_loc[1]]
                environment.info['map'][a_loc[0], a_loc[1]] = _id

        agent_pool.check_arrived(arrived)

        show(f'Simulation of {floor}F_S_{scenario}', environment.info['map'], agent_pool.pool, video_writer)

        if not i % 150:
            num_activate_agents.append(len(agent_pool))
            num_total_agents.append(agent_pool.get_id()-1)
            occupancy_rate.append(round(environment.calc_occupancy() / environment.movable * 100, 4))
            verbose.append(i)

            plot(num_activate_agents, num_total_agents, occupancy_rate, verbose)
            to_csv(num_activate_agents, num_total_agents, occupancy_rate, verbose)

        # wait()
    destroy()
    video_writer.release()