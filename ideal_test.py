# Runs Manning's equations to find water level on a sloped shore, multiple channels, only one section, no redistribution

import pandas as pd
import numpy as np

topo_file = "ideal_topo_1.csv"
storm_file = "ideal_storm_1.csv"

topo = pd.read_csv(topo_file)
roughness = topo["roughness"].to_numpy()
shore_height = topo["shore_height"].to_numpy()
wall_height = topo["wall_height"].to_numpy()
slope = topo["slope"].to_numpy()

surge = pd.read_csv(storm_file)
surge_height = surge["height"].to_numpy()

### INPUT DATA ###
l_seg = 100  # length of a segment
d_seg = 1500  # depth of segment (shore to middle of LM)
dt = 1 * 60 ** 2  # length of a time segment in seconds


h_crit = shore_height + wall_height

volume = np.zeros(surge_height.size)
vel = np.zeros(surge_height.size)
for div in topo["div"]:
    h_diff = surge_height - np.tile(h_crit[div], surge_height.size)
    vel[h_diff > 0] = ((l_seg * h_diff[h_diff > 0]) / (l_seg + 2 * h_diff[h_diff > 0])) ** (2/3) * slope[div] ** (1/2) / roughness[div]
    vel[h_diff < 0] = 0
    if wall_height[div] > 0:
        cwr = 0.611 + 0.075 * h_diff / np.tile(h_crit[div], surge_height.size) 
        vel = vel * cwr
    volume[div] = np.sum(l_seg*dt*h_diff*vel)

total_volume = np.sum(volume)
print (total_volume)
water_height = 2 * total_volume / (d_seg * shore_height.size * l_seg)
print(water_height)
