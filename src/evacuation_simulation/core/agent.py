from random import random, randint

g_id = 0
NEXT = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))


def set_agent_id():
    global g_id
    g_id += 1
    return g_id


class Agent:
    def __init__(self, floor, loc: list[list[int, int]], direction):
        """
        :param floor: Floor where the agent is located
        :param loc: Coordinates where the agent is located
        :param direction: The direction the agent is looking
        """
        self._id = set_agent_id()
        self.floor = floor
        self.location = loc
        self.direction = direction  # 0:N,  1:E,  2:S,  3:W
        self.history = set()

        # if is_adult:
        #     if direction % 2:
        #         self.location.append([loc[0][0] + 1, loc[0][1]])
        #     else:
        #         self.location.append([loc[0][0], loc[0][1] + 1])

    def move(self, r, c):
        self.location = [[loc[0] + r, loc[1] + c] for loc in self.location]

    @property
    def id(self):
        return self._id


class AgentPool:
    def __init__(self, floor, generate_frequency, adult_kids_ratio, random_direction_ration,
                 env):  # check_function, check_direction):
        self.pool = []
        self.floor = [*map(int, floor)]
        self.generate_frequency = generate_frequency
        self.adult_kids_ratio = adult_kids_ratio
        self.random_direction_ration = random_direction_ration
        self.env = env
        # self.check_function = check_function
        # self.check_direction = check_direction
        self._in = 0

    def generate(self, floor, points):
        for point in points:
            if random() < self.generate_frequency:
                direction = randint(0, len(NEXT)-1)
                point = [list(point)]
                if random() < self.adult_kids_ratio:
                    if direction % 2:
                        point.append([point[0][0] + 1, point[0][1]])
                    else:
                        point.append([point[0][0], point[0][1] + 1])
                y, x = NEXT[direction]
                if self.env.check(floor, point, y, x):
                    new_points = [[i + y, j + x] for i, j in point]
                    agent = Agent(floor=floor, loc=new_points, direction=direction)
                    self.env.set_agent(floor=floor, points=agent.location, _id=agent.id)
                    self.pool.append(agent)
                    self._in += 1
                # directions = self.check_direction(floor, point)
                # if directions:
                #     new_dir = randint(0, len(directions) - 1)
                #     y, x = directions[new_dir]

    def move(self, floor):
        for agent in self.pool:

            # self.env.find_next(floor=floor, point=agent.location)
            for b in agent.location:
                agent.history.add(tuple(b))
            y, x = self.env.find_next(floor=floor, point=agent.location, history=agent.history) # if random() > self.random_direction_ration else NEXT[randint(0, 3)]
            # print(y, x)
            if self.env.check(floor=floor, points=agent.location, y=y, x=x):
                self._move(floor=floor, agent=agent, y=y, x=x)
                # before = agent.location
                # agent.move(y, x)
                # self.env.replace_agent(floor=floor, before=before, after=agent.location, _id=agent.id)

            else:
                directions = self.env.check_direction(floor, agent.location)
                if directions:
                    # print(f'agent.location : {agent.location}')
                    # print(f'directions : {directions}')
                    y, x = directions[randint(0, len(directions) - 1)]
                    # print(f'y, x : {y}, {x}')

                    self._move(floor=floor, agent=agent, y=y, x=x)
                    # before = agent.location
                    # agent.move(y, x)
                    # self.env.replace_agent(floor=floor, before=before, after=agent.location, _id=agent.id)

    def _move(self, floor, agent, y, x):
        before = agent.location
        agent.move(y, x)
        self.env.replace_agent(floor=floor, before=before, after=agent.location, _id=agent.id)
