from random import sample
from pathlib import Path

import pandas as pd
import numpy as np

"""
 0 이동 가능
-1 이동 불가
-2 문
 2 집결지
"""


class Environment:
    def __init__(self, _map, floor):
        self.map = {}
        self.dir = ((-1, 0), (0, 1), (1, 0), (0, -1))

        self.floor = floor.split(',')
        prefix = Path(_map)

        for floor in self.floor:
            self.read_map(floor, prefix / f'{floor}f_grid.csv')

    def read_map(self, name, csv):
        _map = pd.read_csv(csv, index_col=0).to_numpy()

        rally_point = np.argwhere(_map == 2)
        entrance = np.argwhere(_map == -2)

        self.map[name] = dict(map=_map, rally_point=rally_point, entrance=entrance)

    def get_spawn_point(self, floor):
        return self.map[floor]['entrance']

    def check(self, floor, points):
        # direction = [self.dir[i] for i in sample(range(4), 4)]
        for y, x in self.dir:
            is_passed = True
            for point in points:
                if self.map[floor]['map'][point[0] + y, point[1] + x]:
                    is_passed = False
            if is_passed:
                return y, x
        return False, False
