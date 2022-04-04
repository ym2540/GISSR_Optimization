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
total_cost, wall_cost = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)
exit()
solutions = [[wall_cost, total_cost, 'N/A', *Wall.heights]]


while wall_cost <= params.budget:
    start_1 = time.time()
    # Calculate change in total cost for each potential allocation
    for sec in range(Wall.segment_count):
        Wall.heights[sec] = Wall.heights[sec] + params.dh
        if sec != 0: Wall.heights[sec-1] = Wall.heights[sec-1] - params.dh
        total_cost_test, wall_cost_test = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)
        marginals[sec] = total_cost - total_cost_test
        wall_costs[sec] = wall_cost_test
        total_costs[sec] = total_cost_test
    # Allocate greedily, update costs and save new point
    print(time.time() - start_1)
    next_allocation = np.argmax(marginals)
    wall_cost = wall_costs[next_allocation]
    solutions.append([wall_cost, total_costs[next_allocation], next_allocation, *Wall.heights])
    Wall.heights[-1] = Wall.heights[-1] - params.dh
    Wall.heights[next_allocation] = Wall.heights[next_allocation] + params.dh
    print(time.time() - start_1)
    print(wall_cost)


solutions_df = pd.DataFrame(solutions)
solutions_df.to_csv('solutions.csv')