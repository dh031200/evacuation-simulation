# SPDX-FileCopyrightText: 2023-present Danny Kim <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .agent import Agent, AgentPool
from .envrionment import Environment


def writer(h, w):
    return cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (w * 2, h * 2))


def show(name, __map, pool, _writer):
    _map = __map.copy()

    if pool:
        _locs = []
        for _id in pool:
            _locs += pool[_id].location
        locs = np.array(_locs)
        _map[locs[:, 0], locs[:, 1]] = 3

    _map = np.repeat(_map, repeats=2, axis=1)
    _map = np.repeat(_map, repeats=2, axis=0)

    h, w = _map.shape

    v_map = np.full((h, w, 3), (0, 0, 0), dtype=np.uint8)
    v_map[_map == -2] = (0, 255, 0)
    v_map[_map == -3] = (255, 0, 0)
    v_map[_map == 0] = (255, 255, 255)
    v_map[_map == 3] = (0, 0, 255)

    _writer.write(v_map)

    cv2.imshow(name, v_map)
    cv2.waitKey(1)


def wait():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def destroy():
    cv2.destroyAllWindows()


def plot(num_activate_agents, num_total_agents, occupancy_rate, verbose):
    plt.title('Occupancy Rate')

    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(verbose, num_activate_agents, color='red', label='Number of Activate Agents')
    ln2 = ax1.plot(verbose, num_total_agents, color='blue', label='Number of Total Agents')
    ax1.set_ylabel('Number of Agents', color='purple', rotation=90)
    ax1.tick_params('y', colors='purple')
    ax1.set_xlabel("Frame")

    ax2 = ax1.twinx()
    ln3 = ax2.plot(verbose, occupancy_rate, color='green', label='Occupancy Rate')
    ax2.set_ylabel('Occupancy Rate (%)', color='green', rotation=90)
    ax2.tick_params('y', colors='green')
    ax2.set_ylim([-5, 100])
    lns = ln1 + ln2 + ln3
    labs = ['Number of Activate Agents', 'Number of Total Agents', 'Occupancy Rate (%)']
    ax1.legend(lns, labs, loc=0)

    plt.tight_layout()
    plt.savefig('occupancy_rate.jpg')
    plt.close()


def to_csv(num_activate_agents, num_total_agents, occupancy_rate, verbose):
    dt = np.array([num_activate_agents, num_total_agents, occupancy_rate]).transpose()
    df = pd.DataFrame(dt, columns=['num_activate_agents', 'num_total_agents', 'occupancy_rate (%)'], index=verbose)
    df['num_activate_agents'] = df['num_activate_agents'].astype(int)
    df['num_total_agents'] = df['num_total_agents'].astype(int)
    df.to_csv('occupancy_rate.csv')


def counts(_map):
    unique, _counts = np.unique(_map.reshape(-1, 3), axis=0, return_counts=True)
    return {tuple(i):v for i, v in zip(unique, _counts)}


__all__ = 'Agent', 'AgentPool', 'Environment', 'show', 'wait', 'destroy', 'writer', 'plot', 'to_csv', 'counts'
