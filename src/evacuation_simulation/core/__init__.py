# SPDX-FileCopyrightText: 2023-present Danny Kim <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
import os

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .agent import AgentPool
from .envrionment import Environment


def mkdir(path):
    os.makedirs(path, exist_ok=True)


def writer(name, h, w, _heatmap=False):
    _heatmap = not _heatmap
    return cv2.VideoWriter(f'{name}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (w * (1 + _heatmap), h * (1 + _heatmap)))


def heatmap(__map):
    _map = __map.copy()
    x_min = _map.min()
    x_max = _map.max()

    _map -= x_min
    _map /= x_max - x_min
    _map *= 255

    dst = cv2.applyColorMap(_map.astype(np.uint8), cv2.COLORMAP_JET)
    cv2.imshow('heatmap', dst)
    return dst


def show(name, __map, pool, num_total_agent, _writer):
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

    cv2.putText(v_map, f'Agents: {num_total_agent}', (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

    _writer.write(v_map)

    cv2.imshow(name, v_map)
    cv2.waitKey(1)


def wait():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def destroy():
    cv2.destroyAllWindows()


def plot(name, num_activate_agents, num_total_agents, occupancy_rate, verbose):
    # plt.title('Occupancy Rate')

    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(verbose, num_activate_agents, color='red', label='Number of Activate Agents')
    # ln2 = ax1.plot(verbose, num_total_agents, color='blue', label='Number of Total Agents')
    ax1.set_ylabel('Number of Agents', color='purple', rotation=90)
    ax1.tick_params('y', colors='red')
    ax1.set_xlabel("Frame")

    ax2 = ax1.twinx()
    ln2 = ax2.plot(verbose, occupancy_rate, color='green', label='Occupancy Rate')
    ax2.set_ylabel('Occupancy Rate (%)', color='green', rotation=90)
    ax2.tick_params('y', colors='green')
    ax2.set_ylim([-5, 100])
    lns = ln1 + ln2
    labs = ['Number of Activate Agents', 'Occupancy Rate (%)']
    # labs = ['Number of Activate Agents', 'Number of Total Agents', 'Occupancy Rate (%)']
    # ax1.legend(lns, labs, loc=0)
    ax1.legend(lns, labs, loc='lower left', bbox_to_anchor=(0.0, 0.0))

    plt.title(f'Simulation   [Total Agent : {num_total_agents[-1]}]')
    plt.tight_layout()
    plt.savefig(f'{name}.jpg')
    plt.close()


def to_csv(name, num_activate_agents, num_total_agents, occupancy_rate, verbose):
    dt = np.array([num_activate_agents, num_total_agents, occupancy_rate]).transpose()
    df = pd.DataFrame(dt, columns=['num_activate_agents', 'num_total_agents', 'occupancy_rate (%)'], index=verbose)
    df['num_activate_agents'] = df['num_activate_agents'].astype(int)
    df['num_total_agents'] = df['num_total_agents'].astype(int)
    df.to_csv(f'{name}.csv')


def counts(_map):
    unique, _counts = np.unique(_map.reshape(-1, 3), axis=0, return_counts=True)
    return {tuple(i): v for i, v in zip(unique, _counts)}


__all__ = 'AgentPool', 'Environment', 'show', 'destroy', 'writer', 'plot', 'to_csv', 'heatmap', 'prefix'
