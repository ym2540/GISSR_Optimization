# Runs Manning's equations to find water level on a sloped shore, multiple channels, only one section, no redistribution

import pandas as pd
import numpy as np

topo_file = "ideal_topo_1.csv"
storm_file = "ideal_storm_1.csv"
div_data_file = "ideal_div_data.csv"

topo = pd.read_csv(topo_file)
div_data = pd.read_csv(div_data_file)
roughness = div_data["roughness"].to_numpy()
shore_height = topo["shore_height"].to_numpy()
wall_height = topo["wall_height"].to_numpy()
slope = div_data["slope"].to_numpy()
divs = div_data["div"].to_numpy()

surge = pd.read_csv(storm_file)
surge_height = surge["height"].to_numpy()

### INPUT DATA ###
l_seg = 100  # length of a segment
dt = 1 * 60 ** 2  # length of a time segment in seconds

h_crit = shore_height + wall_height

volume_div = np.zeros(divs.size)
for div in divs:
    volume_sub = np.zeros(surge_height.size)
    vel = np.zeros(surge_height.size)
    subsections = topo["subsection"].to_numpy()
    subsections = subsections[(topo["div"] == div)]
    print(subsections)
    for subsection in subsections:
        h_diff = surge_height - np.tile(h_crit[subsection], surge_height.size)
        vel[h_diff > 0] = ((l_seg * h_diff[h_diff > 0]) / (l_seg + 2 * h_diff[h_diff > 0])) ** (2/3) * slope[div] ** (1/2) / roughness[div]
        vel[h_diff < 0] = 0
        if wall_height[subsection] > 0:
            cwr = 0.611 + 0.075 * h_diff / np.tile(h_crit[subsection], surge_height.size) 
            vel = vel * cwr
        volume_sub[div] = np.sum(l_seg * dt * h_diff * vel)
    volume_div[div] = np.sum(volume_sub)

print(volume_div)