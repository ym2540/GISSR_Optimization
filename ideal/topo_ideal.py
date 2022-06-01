import pandas as pd
import numpy as np


class Topo:
    def __init__(self, topo_file="Input/ideal_topo_gp_points_1.csv", div_data_file="Input/ideal_div_data.csv", surfaceV_coeff_file="Input/surfaceV_coeff.csv"):
        self.topo = pd.read_csv(topo_file)
        self.div_data = pd.read_csv(div_data_file)
        self.surfaceV_coeff = pd.read_csv(surfaceV_coeff_file)

        self.roughness = self.div_data["roughness"].to_numpy()
        self.shore_height = self.topo["shore_height"].to_numpy(dtype=np.float64)
        self.shore_height_wall = self.topo["shore_height_wall"].to_numpy()
        self.wall_height = self.topo["wall_height"].to_numpy().astype(np.float64)
        self.slope = self.div_data["slope_volume"].to_numpy()
        self.divs = self.div_data["div"].to_numpy()
        self.all_divs = self.topo["div"].to_numpy()
        self.subsections = self.topo["subsection"].to_numpy()
        self.length = self.topo["length"].to_numpy()
        self.slope_manning = self.div_data["slope_manning"].to_numpy()

        self.a = self.surfaceV_coeff["a"].values
        self.b = self.surfaceV_coeff["b"].values
        self.c = self.surfaceV_coeff["c"].values

    def volume_to_height(self, shore_length, volume):
        volume_per_length = volume / shore_length
        height = self.a * np.sqrt(volume_per_length) + self.b * volume_per_length
        height[volume_per_length > (1e8 / (18 * 900))] = self.a * np.sqrt((1e8 / (18 * 900))) + self.b * (1e8 / (18 * 900)) + self.c * (volume_per_length[volume_per_length > (1e8 / (18 * 900))] - (1e8 / (18 * 900)))
        return height
