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

<<<<<<< Updated upstream:run_objective.py

total_cost, wall_cost, df_cost_direct_sum_div_w, h_prop, h = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)
=======
# Calulate initial point
total_cost, wall_cost, df_cost_direct_sum_div_w, fld_h_w, fld_h_w_t = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)



print(fld_h_w)
print(fld_h_w_t)
>>>>>>> Stashed changes:test.py
