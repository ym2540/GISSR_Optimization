# Runs Manning's equations to find water level on a sloped shore, multiple channels, only one section, no redistribution

import pandas as pd
import numpy as np
import time
import itertools as it

from fun_ideal import calc_flood_height, generate_groups, calc_group_vol, calc_group_h
from damage import Damage

topo_file = "ideal_topo_gp_points_1.csv"
storm_file = "surge_w.csv"
div_data_file = "ideal_div_data.csv"
time_file = "time_w.csv"
damage_table_file = "damage_table.csv"

topo = pd.read_csv(topo_file)
surge = pd.read_csv(storm_file).values
div_data = pd.read_csv(div_data_file)
surge_time = pd.read_csv(time_file).values
damage_table = pd.read_csv(damage_table_file)
roughness = div_data["roughness"].to_numpy()
shore_height = topo["shore_height"].to_numpy()
shore_height_wall = topo["shore_height_wall"].to_numpy()
slope = div_data["slope"].to_numpy()
divs = div_data["div"].to_numpy()
subsections = topo["subsection"].to_numpy()

# generate groups
groups = generate_groups(div_data)

segment_l = 100

wall_divs = range(18)

wall_height = np.zeros(shore_height.size)

wall_min = 0
wall_max = 3

wall_points_count = 12 # number of points per dimension
Damage = Damage(damage_table_file)


points_x = it.product(range(wall_points_count), repeat=len(wall_divs))

start = time.time()
points = []
for point_x in points_x:
    heights = wall_min + np.asarray(point_x) * (wall_max - wall_min) / wall_points_count

    wall_height[:] = 0
    positions = []
    for i in range(wall_height.size):
        if topo["div"][i] in wall_divs:
            wall_height[i] = heights[topo["div"][i]]

    height_div, volume_div = calc_flood_height(topo, div_data, surge, surge_time, wall_height)
    volume_grouped = calc_group_vol(groups, volume_div)
    height_group = calc_group_h(topo, div_data, groups, volume_grouped)
    dmg = Damage.calc_damage(height_group)
    cost_dmg = np.sum(dmg)
    cost_wall = np.sum(49212 * wall_height * segment_l)
    cost_tot = cost_dmg + cost_wall

    points.append([*heights, cost_wall, cost_dmg, cost_tot])

df = pd.DataFrame(points)
df.to_csv("gissr_points.csv")
