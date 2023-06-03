from random import random, randint
from scipy.spatial.distance import cdist

import numpy as np

direction = (
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
)


class AgentID:
    def __init__(self):
        self._id = 0

    def get_id(self):
        _id = self._id
        self._id += 1
        return _id


agent_id = AgentID()


class Agent:
    def __init__(self, loc: list[list[int, int]], _direction=None, random_move_ratio=0.2):
        """
        :param loc: Coordinates where the agent is located
        :param _direction: The direction the agent is looking
        :param random_move_ratio: not ideal movement ratio
        """
        self._id = agent_id.get_id()
        self.location = [list(loc)]
        self.direction = _direction  # 0:N,  1:E,  2:S,  3:W
        self.sight = 3
        self.random_move = random_move_ratio

    @property
    def y(self):
        return self.location[0][0]

    @property
    def x(self):
        return self.location[0][1]

    def check(self, area):
        directions = []
        for i, (dy, dx) in enumerate(direction):
            ty, tx = self.sight + dy * self.sight, self.sight + dx * self.sight
            min_x, max_x = min(self.sight + dx, tx), max(self.sight + dx, tx) + 1
            min_y, max_y = min(self.sight + dy, ty), max(self.sight + dy, ty) + 1
            if not area[min_y:max_y, min_x:max_x].all():
                directions.append(i)

        return directions

    def move(self, directions, goal):
        if len(directions):
            if random() < self.random_move:
                r, c = direction[np.random.choice(directions)]
            else:
                t = [(self.y + direction[d][0], self.x + direction[d][1]) for d in directions]
                r, c = direction[np.argmin(cdist(t, goal))]
            self.location = [[loc[0] + r, loc[1] + c] for loc in self.location]


class Adult(Agent):
    def __init__(self, loc: list[list[int, int]], _direction=None, random_move_ratio=0.2):
        super().__init__(loc=loc, _direction=_direction, random_move_ratio=random_move_ratio)

        if _direction % 2:
            self.location.append([self.location[0][0] + 1, self.location[0][1]])
        else:
            self.location.append([self.location[0][0], self.location[0][1] + 1])


class AgentPool:
    def __init__(self, generate_frequency, adult_kids_ratio):
        self.pool = []
        self.generate_frequency = generate_frequency
        self.adult_kids_ratio = adult_kids_ratio
        # self.check_function = check_function

    def generate(self, point):
        if random() < self.generate_frequency:
            if random() < self.adult_kids_ratio:
                self.pool.append(Adult(loc=point))
            else:
                self.pool.append(Agent(loc=point))

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
