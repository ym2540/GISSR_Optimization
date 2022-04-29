#
# THIS CODE IS NOT UP TO DATE AND MAY BE INCOMPATIBLE 
#
#


import pandas as pd
import numpy as np
import itertools as it
import time

from fun_ideal import calc_flood_height, generate_groups, calc_group_vol, calc_group_h
from ideal_damage import Damage
from topo_ideal import Topo

topo_file = "ideal_topo_gp_points_1.csv"
storm_file = "SurgeData/surge_w.csv"
div_data_file = "ideal_div_data.csv"
time_file = "SurgeData/time_w.csv"
damage_table_file = "damage_table.csv"

surge = pd.read_csv(storm_file).values
surge_time = pd.read_csv(time_file).values
damage_table = pd.read_csv(damage_table_file)


Topo = Topo(topo_file=topo_file)
Damage = Damage(damage_table_file)

# generate groups
groups = generate_groups(Topo.div_data)

segment_l = 100

wall_divs = range(18)

wall_height = np.zeros(Topo.shore_height.size)
positions = []
for i, p in enumerate(wall_height):
    if Topo.all_divs[i] in wall_divs:
        positions.append(i)

wall_min = 0
wall_max = 3

wall_points_count = 6 # number of points per dimension


points_x = it.product(range(wall_points_count), repeat=len(wall_divs))

start = time.time()
points = []    
surge_peak = np.amax(surge, axis=1)

for point_x in points_x:
    heights = wall_min + np.asarray(point_x) * (wall_max - wall_min) / wall_points_count

    wall_height[:] = 0

    for i in range(wall_height.size):
        if topo["div"][i] in wall_divs:
            wall_height[i] = heights[topo["div"][i]]
    wall_height[positions] = heights

    height_div, volume_div = calc_flood_height(Topo, surge, surge_time, wall_height, positions)
    volume_grouped = calc_group_vol(groups, volume_div)

    height_group = calc_group_h(Topo, groups, volume_grouped, surge_peak)
    dmg = Damage.calc_damage(height_group)
    cost_dmg = np.sum(dmg)
    cost_wall = np.sum(49212 * wall_height * segment_l)
    cost_tot = cost_dmg + cost_wall

    points.append([*heights, cost_wall, cost_dmg, cost_tot])

df = pd.DataFrame(points)
df.to_csv("gissr_points.csv")
