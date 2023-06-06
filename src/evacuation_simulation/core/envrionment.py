# SPDX-FileCopyrightText: 2023-present Danny Kim <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
from random import choice, random
from pathlib import Path

import pandas as pd
import numpy as np

"""
 0 이동 가능
-1 이동 불가
-2 문
-3 집결지
"""

direction = (
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
)


class Environment:
    def __init__(self, _map, floor, scenario, generate_frequency):
        self.info = None
        self.floor = floor
        self.n_entrance = None
        self.movable = None
        self.frequency_map = None
        self.generate_frequency = generate_frequency
        self.read_map(Path(_map) / f'{floor}f_grid_S_{scenario}.csv')

    @property
    def width(self):
        return self.info['map'].shape[1]

    @property
    def height(self):
        return self.info['map'].shape[0]

    def calc_occupancy(self):
        return len(self.info['map'][self.info['map'] > 0]) + len(self.info['map'][self.info['map'] == -3])

    def read_map(self, csv):
        _map = pd.read_csv(csv, index_col=0).to_numpy()
        self.frequency_map = np.zeros(_map.shape)
        rally_point = np.argwhere(_map == -3)
        entrance = np.argwhere(_map == -2)
        self.movable = len(np.where(_map == 0)[0]) + len(np.where(_map == -3)[0])

        self.info = dict(map=_map, rally_point=rally_point, entrance=entrance)
        self.n_entrance = len(self.info['entrance'])

    def get_spawn_point(self):
        spawn_points = []
        ret = True
        for i in self.info['entrance']:
            spawn_point = []
            for d in direction:
                if not self.info['map'][i[0] + d[0], i[1] + d[1]]:
                    spawn_point.append((i[0] + d[0], i[1] + d[1]))
            if spawn_point:
                spawn_points.append(choice(spawn_point))
        if spawn_points:
            ret = False
        return ret, [i for i in spawn_points if random() < self.generate_frequency]

    @staticmethod
    def get_area(_map, loc, sight):
        min_y, max_y, min_x, max_x = (
            int(1e9),
            -int(1e9),
            int(1e9),
            -int(1e9),
        )
        for _loc in loc:
            min_y = min(min_y, _loc[0])
            max_y = max(max_y, _loc[0])
            min_x = min(min_x, _loc[1])
            max_x = max(max_x, _loc[1])
        return _map[min_y - sight : max_y + sight + 1, min_x - sight : max_x + sight + 1]
