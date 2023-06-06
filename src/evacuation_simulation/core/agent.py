# SPDX-FileCopyrightText: 2023-present Danny Kim <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
from random import random, randint
from scipy.spatial.distance import cdist
from collections import OrderedDict, defaultdict

import numpy as np

direction = (
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
)

direction_dict = {
    (-1, 0): 0,  # up
    (0, 1): 1,  # right
    (1, 0): 2,  # down
    (0, -1): 3,  # left
}

direction_name = {0: 'up', 1: 'right', 2: 'down', 3: 'left'}


class Agent:
    def __init__(self, _id, loc: list[list[int, int]], goal, _direction=None, random_move_ratio=0.2):
        """
        :param loc: Coordinates where the agent is located
        :param _direction: The direction the agent is looking
        :param random_move_ratio: not ideal movement ratio
        """
        self._id = _id
        self.is_adult = False
        self.visited = set()
        self.location = [list(loc)]
        self.goal = goal
        self.direction = _direction  # 0:N,  1:E,  2:S,  3:W
        self.sight = 2
        self.random_move = random_move_ratio
        self.area = None
        self.is_arrive = False
        self.not_moved = [False] * 10
        self.history = defaultdict(int)
        # self.history = np.full((30, 2), (-1, -1), dtype=int)
        # self.history = []
        self.i = 0

    @property
    def y(self):
        return self.location[0][0]

    @property
    def x(self):
        return self.location[0][1]

    @property
    def id(self):
        return self._id

    def check(self, area):
        area[area == self._id] = 0
        self.area = area
        directions = []
        for i, (dy, dx) in enumerate(direction):
            ty, tx = self.sight + dy * self.sight, self.sight + dx * self.sight
            min_x, max_x = min(self.sight + dx, tx), max(self.sight + dx, tx) + 1
            min_y, max_y = min(self.sight + dy, ty), max(self.sight + dy, ty) + 1

            if len(self.location) > 1:
                if i == 0:
                    max_x += 1
                elif i == 1:
                    max_y += 1
                    if not self.direction % 2:
                        min_x += 1
                        max_x += 1
                elif i == 2:
                    max_x += 1
                    if self.direction % 2:
                        min_y += 1
                        max_y += 1
                else:
                    max_y += 1

            if cdist(self.location, self.goal)[0] < 2:
                self.is_arrive = True
            elif len(np.where(area == -3)[0]) > 5:
                self.is_arrive = True
            elif not area[min_y:max_y, min_x:max_x].any():
                directions.append(i)
        return directions

    def move(self, directions):
        self.i += 1
        if len(directions):
            if not self.area.any() and random() < self.random_move:
                r, c = direction[np.random.choice(directions)]
            else:
                t = [(self.y + direction[d][0], self.x + direction[d][1]) for d in directions]
                dists = cdist(t, self.goal)

                sorted_directions = sorted(directions, key=lambda x: dists[directions.index(x)])

                _y, _x = self.location[0]
                _next = []
                for d in sorted_directions:
                    r, c = direction[d]
                    if (_y + r, _x + c) not in self.visited:
                        _next.append(d)

                if _next:
                    r, c = direction[_next[0]]
                else:
                    r, c = direction[np.random.choice(directions)]

            self.direction = direction_dict[(r, c)]
            self.location = [[loc[0] + r, loc[1] + c] for loc in self.location]
            self.visited.add(tuple(self.location[0]))
            self.not_moved[self.i % 10] = False
        else:
            self.not_moved[self.i % 10] = True
        # self.history.append(self.location[0])
        # self.history[self.i % 30] = self.location[0]
        self.history[tuple(self.location[0])] += 1
        return self.location

    def stuck_check(self):
        self.history[tuple(self.location[0])]
        return self.history[tuple(self.location[0])] > 200
        # x, c = np.unique(self.history, return_counts=True, axis=1)
        # if max(c) > 10:
        #     print(f'X: {x}')
        #     print(f'C: {c}')
        # return max(c) > 10


class Adult(Agent):
    def __init__(self, _id, loc: list[list[int, int]], goal, _direction=None, random_move_ratio=0.2):
        super().__init__(_id=_id, loc=loc, goal=goal, _direction=_direction, random_move_ratio=random_move_ratio)
        self.is_adult = True

    def move(self, directions):
        super().move(directions)
        _loc = [self.location[0]]
        if self.direction % 2:
            if not self.area[self.sight + 1, self.sight]:
                _loc.append([self.location[0][0] + 1, self.location[0][1]])
            elif not self.area[self.sight - 1, self.sight]:
                _loc.append([self.location[0][0] - 1, self.location[0][1]])
        else:
            if not self.area[self.sight, self.sight + 1]:
                _loc.append([self.location[0][0], self.location[0][1] + 1])
            elif not self.area[self.sight, self.sight - 1]:
                _loc.append([self.location[0][0], self.location[0][1] - 1])
        self.location = _loc
        return self.location


class AgentPool:
    def __init__(self, goal, adult_kids_ratio, random_move_ratio):
        self._id = 1
        self.pool = OrderedDict()
        self.arrived = []
        self.goal = goal
        # self.generate_frequency = generate_frequency
        self.adult_kids_ratio = adult_kids_ratio
        self.random_move_ratio = random_move_ratio

    def __len__(self):
        return len(self.pool)

    def get_id(self):
        return self._id

    def generate(self, point):
        # print(f'point : {point}')
        # print(f'self.goal : {self.goal}')
        # print(f'cdist([point], self.goal) : {cdist([point], self.goal)}')
        # if random() < self.generate_frequency:
        goal = [self.goal[np.argmin(cdist([point], self.goal))]]
        if random() < self.adult_kids_ratio:
            self.pool[self._id] = Adult(
                _id=self._id,
                loc=point,
                goal=goal,
                _direction=randint(0, 3),
                random_move_ratio=self.random_move_ratio,
            )
        else:
            self.pool[self._id] = Agent(
                _id=self._id,
                loc=point,
                goal=goal,
                _direction=randint(0, 3),
                random_move_ratio=self.random_move_ratio,
            )
        self._id += 1

    def check_arrived(self, arrived):
        for _id in arrived:
            self.arrived.append(self.pool.pop(_id))
