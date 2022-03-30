import pandas as pd
import numpy as np

class Topo:
    def __init__(self, topo_file="LMN_div.csv", roughness_file="Roughness.csv", slope_file="LMN_Slope.csv"):
        self.topo = pd.read_csv(topo_file)
        self.elev = self.topo["MEAN2"]  # coastal elevation
        self.elev_wall = self.topo["MEAN3"]  # elevation where wall would be placed
        self.fid = self.topo["FID"]
        self.div18 = self.topo["DIV18"] 
        self.ndiv18 = np.unique(self.div18).size
        self.roughness = pd.read_csv(roughness_file)["Roughness"]
        self.slope = pd.read_csv(slope_file)["Slope"]
