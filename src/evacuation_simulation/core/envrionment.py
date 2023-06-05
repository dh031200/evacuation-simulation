from random import sample, randint
from pathlib import Path

import pandas as pd
import numpy as np

"""
 0 이동 가능
-1 이동 불가
-2 문
-3 집결지
"""


class Environment:
    def __init__(self, _map, floor, scenario):
        self.info = None
        self.floor = floor
        self.n_entrance = None
        self.movable = None
        self.read_map(Path(_map) / f'{floor}f_grid_S_{scenario}.csv')

    @property
    def width(self):
        return self.info['map'].shape[1]

    @property
    def height(self):
        return self.info['map'].shape[0]

    def calc_occupancy(self):
        return round(len(self.info['map'][self.info['map'] > 0]) + len(self.info['map'][self.info['map'] == -3])*100,3)
        # print(len(self.info['map'][self.info['map'] > 0]))
        # print(self.info['map'][self.info['map'] > 0].shape)

    def read_map(self, csv):
        _map = pd.read_csv(csv, index_col=0).to_numpy()
        # _map = _map[35:35 + 354, 157:157 + 439]
        # pd.DataFrame(_map).to_csv('2f_grid.csv')
        rally_point = np.argwhere(_map == -3)
        entrance = np.argwhere(_map == -2)
        self.movable = len(np.where(_map == 0)[0])

        self.info = dict(map=_map, rally_point=rally_point, entrance=entrance)
        self.n_entrance = len(self.info['entrance'])

    def get_spawn_point(self):
        return self.info['entrance'][randint(0, self.n_entrance - 1)]

    @staticmethod
    def get_area(_map, loc, sight):
        min_y, max_y, min_x, max_x = int(1e9), -int(1e9), int(1e9), -int(1e9),
        for _loc in loc:
            min_y = min(min_y, _loc[0])
            max_y = max(max_y, _loc[0])
            min_x = min(min_x, _loc[1])
            max_x = max(max_x, _loc[1])
        return _map[min_y - sight:max_y + sight + 1, min_x - sight:max_x + sight + 1]

    # def check(self, floor, points):
    #     # direction = [self.dir[i] for i in sample(range(4), 4)]
    #     targets = []
    #     for y, x in self.dir:
    #         for point in points:
    #             if not self.map[floor]['map'][point[0] + y, point[1] + x]:
    #                 targets.append((y, x))
    #
    #     if targets:
    #         targets = targets[randint(0, len(targets) - 1)]
    #
    #     return targets
