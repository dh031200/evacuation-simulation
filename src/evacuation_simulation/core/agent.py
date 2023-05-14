# import numpy as np


class Agent:
    def __init__(self, loc: list[int, int]):
        """
        :param loc: agent location
        """
        self.location = loc

    def move(self, r, c):
        self.location = [self.location[0] + r, self.location + c]
