import time
import numpy as np
from topo import Topo
from damage import Damage 
from wall import Wall


from fun_setup import generate_sv, generate_div_connections
from fun_objective_malloc import objective
import params


SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all = generate_sv()
sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3 = generate_div_connections()

Topo = Topo(params.topo_file, params.roughness_file, params.slope_file)
Wall = Wall(params.wall_positions_file)
Damage = Damage(params.pluto_file, params.fragility_file)


budget = 0
wall_cost = Wall.get_cost()
marginals = np.zeros()

total_cost, wall_cost = objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3)



"""
    budget = 1
    cost_wall = 0
    wall = [0, 0, 0]
    while cost_wall <= budget:
        cost_wall = calc_construction_cost(wall)
        surge = run_gissr(wall)
        cost_damage = calc_damage_cost(surge)
        record_solution(wall, cost_wall, cost_damage, surge)
"""
