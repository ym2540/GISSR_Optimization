import pandas as pd
import numpy as np
import params


class Wall:
    def __init__(self, wall_pos_file):
        self.positions = pd.read_csv(wall_pos_file)["ID"].to_numpy()  # ID of the wall segments, note: not in any particular geographical order
        self.segment_count = self.positions.size
        self.heights = np.ones(self.segment_count)  # Ordered same as positions
        self.cost = 0
        self.div18 = pd.read_csv(wall_pos_file)["div18"].to_numpy() 
        self.segment_l = params.segment_l

    def get_cost(self):
        self.cost = np.sum(109360*self.heights*self.segment_l)
        return self.cost

    def get_nonzero_pos(self):
        self.nonzero_pos = np.ma.masked_where(self.heights <= 0, self.positions).compressed()
        return self.nonzero_pos

    def get_nonzero_heights(self):
        self.nonzero_heights = np.ma.masked_where(self.heights <= 0, self.heights).compressed()
        return self.nonzero_heights