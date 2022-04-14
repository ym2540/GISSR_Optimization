# Runs Manning's equations to find water level on a sloped shore, multiple channels, only one section, no redistribution

import pandas as pd
import numpy as np
import ideal_params as params

from fun_ideal import ideal_water_level, generate_groups, calc_group_vol, calc_group_h

topo_file = "ideal_topo_1.csv"
storm_file = "ideal_storm_1.csv"
div_data_file = "ideal_div_data.csv"

topo = pd.read_csv(topo_file)
surge = pd.read_csv(storm_file)
div_data = pd.read_csv(div_data_file)
roughness = div_data["roughness"].to_numpy()
shore_height = topo["shore_height"].to_numpy()
wall_height = topo["wall_height"].to_numpy().astype(np.float64)
slope = div_data["slope"].to_numpy()
divs = div_data["div"].to_numpy()
subsections = topo["subsection"].to_numpy()

# generate groups
groups = generate_groups(div_data)

######### Run without wall

# height_div, volume_div = ideal_water_level(topo, div_data, surge, wall_height)
# # calculate group volumes
# volume_grouped = calc_group_vol(groups, volume_div)
# # get height in each group
# height_group = calc_group_h(topo, div_data, groups, volume_grouped)
# print(height_group)

########## Allocate to all divisions in divs_allocate simultaniously

# positions = []
# for i, p in enumerate(wall_height):
#     if topo["div"][i] in params.divs_allocate:
#         positions.append(i)

# points = []
# wall_height[positions] = params.h_start
# while wall_height[positions][0] <= params.h_end:
#     height_div, volume_div = ideal_water_level(topo, div_data, surge, wall_height)
#     # calculate group volumes
#     volume_grouped = calc_group_vol(groups, volume_div)
#     # get height in each group
#     height_group = calc_group_h(topo, div_data, groups, volume_grouped)

#     points.append([wall_height[positions][0], *height_div])
#     wall_height[positions] += params.dh

# points_df = pd.DataFrame(points)
# points_df.to_csv("ideal_1d_1.csv")

########### Allocate to all divs , one at a time

all_points = []
all_points.append(np.linspace(params.h_start, params.h_end, num=int((params.h_end - params.h_start) / params.dh) + 1))
for div in params.divs_allocate:
    positions = []
    for i, p in enumerate(wall_height):
        if topo["div"][i] == div:
            positions.append(i)

    points = []
    wall_height[positions] = params.h_start
    while wall_height[positions][0] <= params.h_end:
        height_div, volume_div = ideal_water_level(topo, div_data, surge, wall_height)
        # calculate group volumes
        volume_grouped = calc_group_vol(groups, volume_div)
        # get height in each group
        height_group = calc_group_h(topo, div_data, groups, volume_grouped)

        points.append(height_div[div])
        wall_height[positions] += params.dh

    all_points.append(points)

points_df = pd.DataFrame(all_points).transpose()
points_df.to_csv("ideal_1d_1.csv")

