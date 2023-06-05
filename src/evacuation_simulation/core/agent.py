from random import random, randint
from scipy.spatial.distance import cdist
from collections import OrderedDict

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

direction_name = {0: 'up',
                  1: 'right',
                  2: 'down',
                  3: 'left'}


# class AgentID:
#     def __init__(self):
#         self._id = 0
#
#     def get_id(self):
#         _id = self._id
#         self._id += 1
#         return _id


# agent_id = AgentID()


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

    @property
    def y(self):
        return self.location[0][0]

    @property
    def x(self):
        return self.location[0][1]

    @property
    def id(self):
        return self._id

    # @property
    # def loc(self):
    #     return [i for i in self.location]

    def check(self, area):
        area[area == self._id] = 0
        self.area = area
        # print(area)
        # if -3 in area:
        #     print('goal!!!!!!!')
        directions = []
        # print('-----------------------------')
        # print(self.location)
        # print('sight:')
        # print(area)
        for i, (dy, dx) in enumerate(direction):
            # print(f'enume direction : {direction}')
            # print(f'(dy, dx) : {(dy, dx)}')
            ty, tx = self.sight + dy * self.sight, self.sight + dx * self.sight
            min_x, max_x = min(self.sight + dx, tx), max(self.sight + dx, tx) + 1
            min_y, max_y = min(self.sight + dy, ty), max(self.sight + dy, ty) + 1
            #
            # print(f'min_x : {min_x}')
            # print(f'max_x : {max_x}')
            # print(f'min_y : {min_y}')
            # print(f'max_y : {max_y}')


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


            # if len(self.location) > 1:
            #     zy = self.location[0][0] - self.location[1][0]
            #     zx = self.location[0][1] - self.location[1][1]
            #     print(f'zy, zx : {zy}, {zx}')
            #     # print(zy, zx)
            #     if i % 2:
            #         max_y += 1
            #         min_x += zx
            #         max_x += zx
            #     else:
            #         max_x += 1
            #         min_y += zy
            #         max_y += zy

                # if i == 0:
                #     max_x += 1
                # elif i == 1:
                #     max_y += 1
                #     if not self.direction % 2:
                #         min_x += 1
                #         max_x += 1
                # elif i == 2:
                #     max_x += 1
                #     if self.direction % 2:
                #         min_y += 1
                #         max_y += 1
                # else:
                #     max_y += 1

            #     print('adult:')
            #     print(f'min_x : {min_x}')
            #     print(f'max_x : {max_x}')
            #     print(f'min_y : {min_y}')
            #     print(f'max_y : {max_y}')
            # print(area[min_y:max_y, min_x:max_x])
            # print(area[min_y:max_y, min_x:max_x].any())
            # print('====================================')
            # if len(self.location) > 1:
            #     zy, zx = abs(self.location[0][0] - self.location[1][0]), abs(self.location[0][1] - self.location[1][1])

            # print(f'dy, dx : {dy}, {dx}')
            # print(f'area[min_y:max_y, min_x:max_x] : {area[min_y:max_y, min_x:max_x]}')
            # print(f'area[min_y:max_y, min_x:max_x].any() : {area[min_y:max_y, min_x:max_x].any()}')
            # if -3 in area[min_y:max_y, min_x:max_x]:
            #     self.is_arrive = True
            # print(area[1:-1,1:-1])
            if cdist(self.location, self.goal)[0] < 2:
                self.is_arrive = True
            elif len(np.where(area == -3)[0]) > 5:
                self.is_arrive = True
            elif not area[min_y:max_y, min_x:max_x].any():
                directions.append(i)
        # print('--------------------------')
        # print(f'directions : {[direction_name[j] for j in directions]}')
        return directions

    def move(self, directions):
        if len(directions):
            if not self.area.any() and random() < self.random_move:
                r, c = direction[np.random.choice(directions)]
            else:
                t = [(self.y + direction[d][0], self.x + direction[d][1]) for d in directions]
                dists = cdist(t, self.goal)

                sorted_directions = sorted(directions, key=lambda x: dists[directions.index(x)])
                # print(f'sorted_directions : {sorted_directions}')

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

                # print(f'r, c : {r}, {c}')
                    # r, c = 0, 0

                # best = np.argmin(cdist(t, goal))
                # r, c = direction[directions[best]]
                # _y, _x = self.location[0]
                # if (_y + r, _x + c) in self.visited:
                #     directions.pop(best)
                #     best = np.argmin(cdist(t, goal))

                # print(f't : {t}')
                # print(f'goal : {goal}')
                # print(f'cdist(t, goal) : {cdist(t, goal)}')
                # print(f'np.argmin(cdist(t, goal)) : {np.argmin(cdist(t, goal))}')
            # print(f'r, c : {r}, {c}')
            # _y, _x = self.location[0]
            # if (_y + r, _x + c) in self.visited and random() < 0.8:
            #     # directions.pop(best)
            #     r, c = direction[np.random.choice(directions)]
            # print(f'r, c : {r}, {c}')
            self.direction = direction_dict[(r, c)]
            # print(f'go {direction_name[self.direction]}')
            # print(f'direction : {self.direction}')
            self.location = [[loc[0] + r, loc[1] + c] for loc in self.location]
            self.visited.add(tuple(self.location[0]))
        # return self.location


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
        # return self.location


class AgentPool:
    def __init__(self, generate_frequency, goal, adult_kids_ratio, random_move_ratio):
        self._id = 1
        self.pool = OrderedDict()
        self.arrived = []
        self.goal = goal
        self.generate_frequency = generate_frequency
        self.adult_kids_ratio = adult_kids_ratio
        self.random_move_ratio = random_move_ratio
        # self.check_function = check_function

    def get_id(self):
        return self._id

    def generate(self, point):
        if random() < self.generate_frequency:
            goal = [self.goal[np.argmin(cdist([point], self.goal))]]
            if random() < self.adult_kids_ratio:
                self.pool[self._id] = Adult(_id=self._id, loc=point, goal=goal, _direction=randint(0, 3),
                                            random_move_ratio=self.random_move_ratio)
                # self.pool.append(Adult(_id=self.get_id(), loc=point, _direction=randint(0, 3),
                #                        random_move_ratio=self.random_move_ratio))
            else:
                self.pool[self._id] = Agent(_id=self._id, loc=point, goal=goal, _direction=randint(0, 3),
                                            random_move_ratio=self.random_move_ratio)
            self._id += 1
            # self.pool.append(Agent(_id=self.get_id(), loc=point, _direction=randint(0, 3),
            #                        random_move_ratio=self.random_move_ratio))

    def check_arrived(self, arrived):
        # print(f'self.pool : {self.pool}')
        for _id in arrived:
            self.arrived.append(self.pool.pop(_id))

    # def generate(self, floor, points):
    #     for point in points:
    #         if random() < self.generate_frequency:
    #             direction = randint(0, 3)
    #             point = [list(point)]
    #             if random() < self.adult_kids_ratio:
    #                 if direction % 2:
    #                     point.append([point[0][0] + 1, point[0][1]])
    #                 else:
    #                     point.append([point[0][0], point[0][1] + 1])
    #             y, x = self.check_function(floor, point)
    #             if any([y, x]):
    #                 new_points = [[i + y, j + x] for i, j in point]
    #                 agent = Agent(floor=floor, loc=new_points, direction=direction)
    #                 self.pool.append(agent)

    # def move(self, floor):
    #     for agent in self.pool:
    #         _next = self.check_function(floor, agent.location)
    #         if _next:
    #             agent.move(*_next)
