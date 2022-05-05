import pandas as pd
import numpy as np

class Topo:
    def __init__(self, topo_file="Input/ideal_topo_gp_points_1.csv", div_data_file="Input/ideal_div_data.csv"):
        self.topo = pd.read_csv(topo_file)
        self.div_data = pd.read_csv(div_data_file)
        self.roughness = self.div_data["roughness"].to_numpy()
        self.shore_height = self.topo["shore_height"].to_numpy(dtype=np.float64)
        self.shore_height_wall = self.topo["shore_height_wall"].to_numpy()
        self.wall_height = self.topo["wall_height"].to_numpy().astype(np.float64)
        self.slope = self.div_data["slope"].to_numpy()
        self.divs = self.div_data["div"].to_numpy()
        self.all_divs = self.topo["div"].to_numpy()
        self.subsections = self.topo["subsection"].to_numpy()

