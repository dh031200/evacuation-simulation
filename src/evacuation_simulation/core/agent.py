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
    def __init__(self, _id, loc: list[list[int, int]], goal, _direction=None, random_move_ratio=0.2, fr=None):
        """
        :param loc: Coordinates where the agent is located
        :param _direction: The direction the agent is looking
        :param random_move_ratio: not ideal movement ratio
        """
        # self.fr = fr
        self._id = _id
        self.is_adult = False
        self.visited = set()
        self.location = [list(loc)]
        # self.goal = goal
        if fr:
            self.goal = [fr] + goal
        else:
            self.goal = goal
        self.direction = _direction  # 0:N,  1:E,  2:S,  3:W
        self.sight = 2
        self.random_move = random_move_ratio
        self.area = None
        self.is_arrive = False
        self.not_moved = [False] * 30
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

            if cdist(self.location, self.goal)[0][0] < (2 + ((len(self.goal) - 1) * 4)):
                del self.goal[0]
                # print(f'self.goal : {self.goal}')
                if not self.goal:
                    self.is_arrive = True
                    break
            elif len(np.where(area == -3)[0]) > 5:
                self.is_arrive = True
            elif not area[min_y:max_y, min_x:max_x].any():
                directions.append(i)
        return directions

    def move(self, directions, stuck):
        self.i += 1
        # print(f'current : {self.location}')
        # print(f'directions : {directions}')
        if len(directions):
            if not self.area.any() and random() < self.random_move:
                _next = [np.random.choice(directions)]
            elif stuck:
                # print('random_move')
                _next = []
                # for i, _loc in self.location[0]:
                _y, _x = self.location[0]
                for d in directions:
                    r, c = direction[d]
                    if (_y + r, _x + c) not in self.visited:
                        _next.append(d)

                # _next = [set(), set()]
                # for i, _loc in enumerate(self.location):
                #     _y, _x = _loc
                #
                #     for d in directions:
                #         r, c = direction[d]
                #         if (_y + r, _x + c) not in self.visited:
                #             _next[i].add(d)
                # _next = _next[0].intersection(_next[1])

            else:
                # print('distance_base')
                t = [(self.y + direction[d][0], self.x + direction[d][1]) for d in directions]
                dists = cdist(t, self.goal)

                sorted_directions = sorted(directions, key=lambda x: dists[directions.index(x)][0])
                # print(f'sorted_directions : {sorted_directions}')
                # print(f'self.visited: {self.visited}')
                _next = []
                # for i, _loc in enumerate(self.location):
                _y, _x = self.location[0]
                for d in sorted_directions:
                    r, c = direction[d]
                    if (_y + r, _x + c) not in self.visited:
                        # print(f'OOO {(_y + r, _x + c)} not in self.visited')
                        _next.append(d)
                    # else:
                    # print(f'XXX {(_y + r, _x + c)} in self.visited')

                # _next = [set(), set()]
                # for i, _loc in enumerate(self.location):
                #     _y, _x = _loc
                #     for d in sorted_directions:
                #         r, c = direction[d]
                #         if (_y + r, _x + c) not in self.visited:
                #             print(f'OOO {(_y + r, _x + c)} not in self.visited')
                #             _next[i].add(d)
                #         else:
                #             print(f'XXX {(_y + r, _x + c)} in self.visited')
                # _next = _next[0].intersection(_next[1])
            # print(f'_next : {_next}')
            _next = list(_next)
            if _next:
                frequency = [_next[0]] * 9
                r, c = direction[np.random.choice(frequency + _next[:2])]
            else:
                r, c = direction[np.random.choice(directions)]

            self.direction = direction_dict[(r, c)]
            self.location = [[loc[0] + r, loc[1] + c] for loc in self.location]
            # loc = []
            # print(f'r : {r}, c : {c}')
            # for _loc in self.location:
            #     __loc = (_loc[0] + r, _loc[1] + c)
            #     loc.append(__loc)
            #     self.visited.add(__loc)
            # self.location = loc
            self.visited.add(tuple(self.location[0]))
            # self.visited.add(tuple(self.location[1]))
            # if tuple(self.location[0]) == (292, 255):
            # print('now')
            self.not_moved[self.i % 30] = False
        else:
            self.not_moved[self.i % 30] = True
        # else:
        # self.not_moved[self.i % 30] = True
        # self.history.append(self.location[0])
        # self.history[self.i % 30] = self.location[0]
        self.history[tuple(self.location[0])] += 1
        # print('-------------------------------------')
        return self.location

    def stuck_check(self, area):
        # self.history[tuple(self.location[0])]
        return (self.history[tuple(self.location[0])] > 100) and (len(np.where(area == -3)[0]) > 2)
        # x, c = np.unique(self.history, return_counts=True, axis=1)
        # if max(c) > 10:
        #     print(f'X: {x}')
        #     print(f'C: {c}')
        # return max(c) > 10


class Adult(Agent):
    def __init__(self, _id, loc: list[list[int, int]], goal, _direction=None, random_move_ratio=0.2, fr=None):
        super().__init__(_id=_id, loc=loc, goal=goal, _direction=_direction, random_move_ratio=random_move_ratio, fr=fr)
        self.is_adult = True

    def move(self, directions, stuck):
        super().move(directions, stuck)
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
        # print(f'point : {point}')
        fr = None
        if (point[0] == 200) and (113 <= point[1] <= 134):
            fr = (296, 155)
        elif (point[0] == 200) and (139 <= point[1] <= 240):
            fr = (224, 302)
        elif (200 <= point[0] <= 221) and (point[1] == 240):
            fr = (224, 302)
        elif (283 <= point[0] <= 297) and (point[1] == 178):
            fr = (279, 129)
        # elif (215 <= point[0] <= 226) and (point[1] == 432):
        #     fr = (151, 348)
        if random() < self.adult_kids_ratio:
            self.pool[self._id] = Adult(
                _id=self._id,
                loc=point,
                goal=goal,
                _direction=randint(0, 3),
                random_move_ratio=self.random_move_ratio,
                fr=fr,
            )
        else:
            self.pool[self._id] = Agent(
                _id=self._id,
                loc=point,
                goal=goal,
                _direction=randint(0, 3),
                random_move_ratio=self.random_move_ratio,
                fr=fr,
            )
        self._id += 1

    def check_arrived(self, arrived):
        for _id in arrived:
            self.arrived.append(self.pool.pop(_id))
