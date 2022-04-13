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
subsections = topo["subsection"].to_numpy()

surge = pd.read_csv(storm_file)
surge_height = surge["height"].to_numpy()
surge_peak = np.max(surge_height)

### INPUT DATA ###
l_seg = 100  # length of a segment
dt = 1 * 60 ** 2  # length of a time segment in seconds
travel_dist = 2  # number of adjacent divisions (in one direction) that water can be redistributed to 

h_crit = shore_height + wall_height

volume_div = np.zeros(divs.size)
height_div = np.zeros(divs.size)
for div in divs:
    vel = np.zeros(surge_height.size)
    subsections_div = subsections[(topo["div"] == div)]
    volume_sub = np.zeros(subsections_div.size)
    for i, subsection in enumerate(subsections_div):
        h_diff = surge_height - np.tile(h_crit[subsection], surge_height.size)
        vel[h_diff > 0] = ((l_seg * h_diff[h_diff > 0]) / (l_seg + 2 * h_diff[h_diff > 0])) ** (2/3) * slope[div] ** (1/2) / roughness[div]
        vel[h_diff < 0] = 0
        if wall_height[subsection] > 0:
            cwr = 0.611 + 0.075 * h_diff / np.tile(h_crit[subsection], surge_height.size) 
            vel = vel * cwr
        volume_sub[i] = np.sum(l_seg * dt * h_diff * vel)
    volume_div[div] = np.sum(volume_sub)

    # Limit water level to surge peak
    max_volume = (subsections_div.size * l_seg * surge_peak**2) / (2 * slope[div])
    if volume_div[div] > max_volume:
        volume_div[div] = max_volume
    height_div[div] = np.sqrt((2 * volume_div[div] * slope[div]) / (l_seg * subsections_div.size))

# generate groups
groups = []
for d in divs:
    start = d - travel_dist  # start of group, inclusive
    if d < travel_dist:
        start = 0

    end = d + travel_dist  # end of group, inclusive
    if d + travel_dist > divs.size:
        end = divs.size - 1

    group = divs[start:end+1]
    groups.append((group, group.size))

# calculate group volumes
volume_grouped = np.zeros(divs.size)
for v in range(volume_grouped.size):
    volume_grouped[v] = np.sum(volume_div[groups[v][0]])

# get height in each group
height_group = np.zeros(divs.size)
for h in range(height_group.size):
    avg_slope = np.mean(slope[groups[h][0]])
    num_subsections = [i for i, div in enumerate(topo["div"]) if div in groups[h][0]]
    group_length = len(num_subsections) * l_seg
    height_group[h] = np.sqrt((2 * volume_grouped[h] * avg_slope) / group_length)  # assumes 8 segments per div for now

print(height_group)