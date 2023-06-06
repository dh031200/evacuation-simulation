# SPDX-FileCopyrightText: 2023-present Danny Kim <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from evacuation_simulation.__about__ import __version__
from evacuation_simulation import AgentPool, Environment, show, destroy, writer, plot, to_csv, heatmap, mkdir


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="Evacuation-Simulation")
@click.option('--map_dir', '-m', required=True, help='map directory')
@click.option('--floor', '-f', required=True, help='floor for simulation')
@click.option('--scenario', '-s', required=True, help='scenario for simulation')
def evacuation_simulation(map_dir, floor, scenario):
    click.echo("Hello world!")
    environment = Environment(map_dir, floor, scenario, generate_frequency=0.01)
    agent_pool = AgentPool(goal=environment.info['rally_point'], adult_kids_ratio=0.7, random_move_ratio=0.2)
    _map = environment.info['map'].copy()
    simulation_name = f'{floor}F_S_{scenario}'
    prefix = f'{simulation_name}/'
    mkdir(prefix)
    simulation_writer = writer(f'{prefix}{simulation_name}_simulation', environment.height, environment.width)
    heatmap_writer = writer(f'{prefix}{simulation_name}_heatmap', environment.height, environment.width, _heatmap=True)
    occupancy_rate = []
    verbose = []
    num_activate_agents = []
    num_total_agents = []
    show(f'Simulation of {simulation_name}', environment.info['map'], agent_pool.pool, 0, simulation_writer)

    mem = [False] * 10
    i = 0
    while True:
        i += 1
        ret, spawn_points = environment.get_spawn_point()
        mem[i % 10] = ret
        if sum(mem) == 10:
            break
        for spawn_point in spawn_points:
            agent_pool.generate(spawn_point)

        arrived = []
        for _id in agent_pool.pool:
            agent = agent_pool.pool[_id]
            area = environment.get_area(environment.info['map'], agent.location, agent.sight)
            _next = agent.check(area)
            if agent.is_arrive:
                for _loc in agent.location:
                    environment.info['map'][_loc[0], _loc[1]] = -3

                arrived.append(agent.id)
                continue
            before = agent.location
            # agent.move(_next)
            coords = agent.move(_next)
            if sum(agent.not_moved) == 30 or agent.stuck_check(area):
                for _loc in agent.location:
                    environment.info['map'][_loc[0], _loc[1]] = -3
                arrived.append(agent.id)
                continue
            for coord in coords:
                environment.frequency_map[coord[0], coord[1]] += 1
            for b_loc, a_loc in zip(before, agent.location):
                environment.info['map'][b_loc[0], b_loc[1]] = _map[b_loc[0], b_loc[1]]
                environment.info['map'][a_loc[0], a_loc[1]] = _id
                # environment.frequency_map[a_loc[0], a_loc[1]] += 1

        agent_pool.check_arrived(arrived)
        total_agent = agent_pool.get_id() - 1

        show(
            f'Simulation of {simulation_name}', environment.info['map'], agent_pool.pool, total_agent, simulation_writer
        )
        heatmap_writer.write(heatmap(environment.frequency_map))

        if not i % 150:
            num_activate_agents.append(len(agent_pool))
            num_total_agents.append(agent_pool.get_id() - 1)
            occupancy_rate.append(round(environment.calc_occupancy() / environment.movable * 100, 4))
            verbose.append(i)

            plot(prefix + simulation_name, num_activate_agents, num_total_agents, occupancy_rate, verbose)
            to_csv(prefix + simulation_name, num_activate_agents, num_total_agents, occupancy_rate, verbose)

    destroy()
    simulation_writer.release()
    heatmap_writer.release()
