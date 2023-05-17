from pathlib import Path

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from random import random, randint

"""
 0 이동 가능
-1 이동 불가
-2 문
 2 집결지
"""


class Environment:
    def __init__(self, _map, floor):
        self.map = {}
        self.board = {}
        self.dir = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))

        self.floor = floor.split(',')
        prefix = Path(_map)

        for floor in self.floor:
            self.read_map(floor, prefix / f'{floor}f_grid.csv')

    def read_map(self, name, csv):
        _map = pd.read_csv(csv, index_col=0).to_numpy()
        _map[_map == 2] = -3

        rally_point = np.argwhere(_map == -3)
        entrance = np.argwhere(_map == -2)

        height, width = _map.shape
        self.board[name] = _map.copy()

        self.map[name] = dict(map=_map, rally_point=rally_point, entrance=entrance, height=height, width=width)

    def replace_agent(self, floor, before, after, _id):
        for b, a in zip(before, after):
            self.board[floor][b[0], b[1]] = 0
            self.board[floor][a[0], a[1]] = _id

    def set_agent(self, floor, points, _id):
        for point in points:
            self.board[floor][point[0], point[1]] = _id

    def get_spawn_point(self, floor):
        return self.map[floor]['entrance']

    def check(self, floor, points, y, x):
        is_passed = True
        for point in points:
            if any([0 > point[0] + y, point[0] + y >= self.map[floor]['height'],
                    0 > point[1] + x, point[1] + x >= self.map[floor]['width']]) or self.board[floor][
                point[0] + y, point[1] + x]:
                is_passed = False
        return is_passed

    def check_direction(self, floor, points):
        directions = []
        for y, x in self.dir:
            if self.check(floor=floor, points=points, y=y, x=x):
                directions.append([y, x])
        return directions

    def assign(self, floor, pool):
        self.board[floor] = self.map[floor]['map'].copy()
        for agent in pool:
            for loc in agent.location:
                self.board[floor][loc[0], loc[1]] = agent.id

    def find_next(self, floor, point, history):
        # row, col = point[0]
        # print(point)
        # print(f'self.map[floor]["rally_point"] : {self.map[floor]["rally_point"]}')
        distance = cdist([point[0]], self.map[floor]['rally_point'])
        rally_idx = np.argmin(distance[0])
        # print(f'distance: {distance}')
        # print(self.map[floor]['rally_point'][np.argmin(distance[0])])
        y, x = point[0]

        # for _r,_c in [[y + r * 2, x + c * 2] for r, c in self.dir]:
        #     self.check()
        # c_points = []
        is_passed = []
        for i, (_r, _c) in enumerate(self.dir):
            # if self.check(floor=floor, points=point, y=_r * 2, x=_c * 2) & self.check(floor=floor, points=point, y=_r * 3, x=_c * 3):
            if self.check(floor=floor, points=point, y=_r * 3, x=_c * 3):
                is_passed.append(i)

        c_points = [[y + r, x + c] for r, c in self.dir]

        # c_points = [[y + r * 2, x + c * 2] for r, c in self.dir]

        # if random() < 0.3:
        #     c_points = [[y + r, x + c] for r, c in self.dir]
        # else:
        #     c_points = []
        #     for r, c in self.dir:
        #         if (y + r, x + c) not in history:
        #             c_points.append([y + r, x + c])
        # print(cdist(c_points, [self.map[floor]['rally_point'][rally_idx]]))
        # distance = {v:i for i,v in enumerate(cdist(c_points, [self.map[floor]['rally_point'][rally_idx]]))}
        # print(distance)
        # print(sorted(distance))
        distance = cdist(c_points, [self.map[floor]['rally_point'][rally_idx]])
        targets = [i for i in sorted(range(8), key=lambda x: distance[x])[:3] if i in is_passed]
        # print(targets)
        if targets:
            return self.dir[targets[randint(0, len(targets)-1)]]
        else:
            if is_passed:
                return self.dir[is_passed[randint(0,len(is_passed)-1)]]
            else:
                return self.dir[randint(0,7)]
        # sorted(distance)

        # if c_points:
        #     distance = cdist(c_points, [self.map[floor]['rally_point'][rally_idx]])
        #     return self.dir[np.argmin(distance)]
        # else:
        #     return 0, 0
