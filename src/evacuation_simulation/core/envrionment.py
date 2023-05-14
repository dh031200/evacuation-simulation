from pathlib import Path

import pandas as pd


class Environment:
    def __init__(self):
        self.map = {}
        prefix = Path(__file__).parent / '..' / 'map'
        print(prefix)
        # print(os.listdir())
        self.read_map('2nd', prefix / '2f_grid.csv')
        self.read_map('3rd', prefix / '3f_grid.csv')

    def read_map(self, name, csv):
        _map = pd.read_csv(csv, index_col=0).to_numpy()
        # _map = np.repeat(_map, repeats=2, axis=1)
        # _map = np.repeat(_map, repeats=2, axis=0)
        self.map[name] = _map
