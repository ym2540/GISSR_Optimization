import time
import numpy as np
import pandas as pd
from topo import Topo
from damage import Damage 
from wall import Wall


from fun_setup import generate_sv, generate_div_connections
from fun_objective_malloc import objective
import params

######### Initialize Sections and Surface Volume Functions #########
SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all = generate_sv()
sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3 = generate_div_connections()

######### Get Topography, Wall, and Damage Model #########
Topo = Topo(params.topo_file, params.roughness_file, params.slope_file)
Wall = Wall(params.wall_positions_file)
Damage = Damage(params.pluto_file, params.fragility_file)

wall_cost = Wall.get_cost()
marginals = np.zeros(Wall.segment_count)
wall_costs = np.zeros(Wall.segment_count)
total_costs = np.zeros(Wall.segment_count)

# Calulate initial point
print("------------WITHOUT WALL---------------")
total_cost, wall_cost, cost_by_div, h, h_prop = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)
#points = [[0, wall_cost, total_cost, *cost_by_div["dirct_cost"].values.tolist()]]
# print("total cost: "+ str(total_cost[0]))
# print("total cost sum: " + str(sum(cost_by_div["dirct_cost"].to_numpy())))
print(h)
print(h_prop)
positions = pd.read_csv(params.wall_positions_file)
for i in range(Wall.heights.size):
    if positions['div18'].to_numpy()[i] in [13, 16, 1]:
        Wall.heights[i] = 3
print("------------WITH WALL---------------")
total_cost_new, wall_cost_new, cost_by_div_new, h_new, h_prop_new = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)
#points = [[0, wall_cost, total_cost, *cost_by_div["dirct_cost"].values.tolist()]]
# print("total cost: "+ str(total_cost_new[0]))
# print("total cost sum: " + str(sum(cost_by_div_new["dirct_cost"].to_numpy())))
print(h_new)
print(h_prop_new)
print("------------ DIFF ---------------")
print(cost_by_div_new["dirct_cost"].to_numpy() - cost_by_div["dirct_cost"].to_numpy())
diff = h_new - h
diff2 = h_prop_new - h_prop
print(pd.DataFrame(data=diff.flatten(), index=range(diff.size)))
print(pd.DataFrame(data=diff2.flatten(), index=range(diff2.size)))
exit()





subsection = 50
while Wall.heights[subsection] <= 5:
    print(Wall.heights[subsection])
    Wall.heights[subsection] += params.dh
    total_cost, wall_cost, cost_by_div = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)
    points.append([Wall.heights[subsection], wall_cost, total_cost, *cost_by_div["dirct_cost"].values.tolist()])

points_df = pd.DataFrame(points)
points_df.to_csv("points_1d.csv")