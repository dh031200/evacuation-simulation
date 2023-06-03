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
        self.read_map(Path(_map) / f'{floor}f_grid_S_{scenario}.csv')

    def read_map(self, csv):
        _map = pd.read_csv(csv, index_col=0).to_numpy()
        # _map = _map[35:35 + 354, 157:157 + 439]
        # pd.DataFrame(_map).to_csv('2f_grid.csv')
        rally_point = np.argwhere(_map == -3)
        entrance = np.argwhere(_map == -2)

        self.info = dict(map=_map, rally_point=rally_point, entrance=entrance)
        self.n_entrance = len(self.info['entrance'])

    def get_spawn_point(self):
        return self.info['entrance'][randint(0, self.n_entrance - 1)]

    def get_area(self, loc, sight):
        y, x = loc[0]
        return self.info['map'][y - sight:y + sight + 1, x - sight:x + sight + 1]

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
