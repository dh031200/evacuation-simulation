from random import random, randint


class Agent:
    def __init__(self, floor, loc: list[list[int, int]], direction):
        """
        :param floor: Floor where the agent is located
        :param loc: Coordinates where the agent is located
        :param direction: The direction the agent is looking
        """
        self.floor = floor
        self.location = loc
        self.direction = direction  # 0:N,  1:E,  2:S,  3:W

    def move(self, r, c):
        self.location = [[loc[0] + r, loc[1] + c] for loc in self.location]


class AgentPool:
    def __init__(self, floor, generate_frequency, adult_kids_ratio, check_function):
        self.pool = []
        self.floor = [*map(int, floor)]
        self.generate_frequency = generate_frequency
        self.adult_kids_ratio = adult_kids_ratio
        self.check_function = check_function

    def generate(self, floor, points):
        for point in points:
            if random() < self.generate_frequency:
                direction = randint(0, 3)
                point = [list(point)]
                if random() < self.adult_kids_ratio:
                    if direction % 2:
                        point.append([point[0][0] + 1, point[0][1]])
                    else:
                        point.append([point[0][0], point[0][1] + 1])
                y, x = self.check_function(floor, point)
                if any([y, x]):
                    new_points = [[i + y, j + x] for i, j in point]
                    agent = Agent(floor=floor, loc=new_points, direction=direction)
                    self.pool.append(agent)

    def move(self, floor):
        for agent in self.pool:
            _next = self.check_function(floor, agent.location)
            if _next:
                agent.move(*_next)
