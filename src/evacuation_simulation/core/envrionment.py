import pandas as pd

# import numpy as np


class Environment:
    def __init__(self):
        self.map = []
        self.read_map('..map/2f_grid.csv')
        self.read_map('..map/3f_grid.csv')

    def read_map(self, csv):
        self.map.append(pd.read_csv(csv, index_col=0).to_numpy())
