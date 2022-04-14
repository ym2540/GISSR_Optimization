import numpy as np
import pandas as pd
import time

# import functions 
from fun_floodestimate import FloodHeightWall, FloodTravelSectGroup
import params

pd.options.mode.chained_assignment = None  # default='warn'


def objective(Topo, Wall, Damage, SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20,
              SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20,
              SV_all, sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3):

    ###################### DATA #################################

    ftm = params.ftm
    nt = params.nt

    ###################### MAIN #################################
    wall_cost = Wall.get_cost()
    wall_positions = Wall.get_nonzero_pos()
    wall_heights = Wall.get_nonzero_heights()  # mask positions with height==0
    foo = pd.DataFrame(wall_heights)
    foo.to_csv("foo.csv")
    exit()
    
    elev = Topo.elev
    if wall_positions.size != 0:
        elev[wall_positions] = Topo.elev_wall[wall_positions] + wall_heights

    # Arays used for multiple storms
    # n_damage_loss_w = []
    # n_cost_util_w = []
    # n_cost_tran_w = []

    sandy_surge = pd.read_csv(
        r"CO-OPS_8518750_met_hr.csv")['Verified (m)'].values.transpose()

    time1 = np.reshape(np.linspace(0, 23, 24), (1, 24))
    time2 = np.reshape(np.linspace(24, 47, 24), (1, 24))

    cpi1_w = np.reshape(sandy_surge[:24], (1, 24))
    cpi2_w = np.reshape(sandy_surge[24:], (1, 24))
    peak_w = max(sandy_surge)
    peak_w = peak_w.reshape((peak_w.size,))

    fld_h_w = np.zeros((np.shape(cpi1_w)[0], params.ndiv18))
    V_w = np.zeros((np.shape(cpi1_w)[0], params.ndiv18))
    for i in range(params.ndiv18):
        fld_h_w[:, i], V_w[:, i] = FloodHeightWall(SV_all[i], wall_positions, Topo.slope[i], Topo.roughness[i], SVf1[i, :], SVf2[i, :], SVf3[i, :], SVf4[i, :], SVf5[i, :], SVf6[i, :], SVf7[i, :], SVf8[i, :], SVf9[i, :], SVf10[i, :],
                                                   SVf11[i, :], SVf12[i, :], SVf13[i, :], SVf14[i, :], SVf15[i, :], SVf16[i, :], SVf17[i, :], SVf18[i, :], SVf19[i, :], SVf20[i, :], time1, time2, cpi1_w, cpi2_w, nt, elev[Topo.div18 == i], Topo.fid[Topo.div18 == i], params.segment_l, peak_w, i)

    fld_h_w_sect_g, V_w_sect_avr = FloodTravelSectGroup(SV_all, params.ndiv18, peak_w, sect0, sect1, sect2, sect3, sect_3, sect_2, sect_1, V_w, SVfg1, SVfg2,
                                                        SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20)

    damage_loss_w, inop_util_w, inop_tran_w, cost_util_w, cost_tran_w, df_cost_direct_sum_div_w = Damage.dmg_cost_vector(fld_h_w_sect_g/ftm)
    
    ##### Only needed for multiple storms
    # n_damage_loss_w = np.append(n_damage_loss_w, np.sum(damage_loss_w))
    # n_cost_util_w = np.append(n_cost_util_w, np.sum(inop_util_w))
    # n_cost_tran_w = np.append(n_cost_tran_w, np.sum(cost_tran_w))
    # mean_damage_loss_w = np.mean(n_damage_loss_w)
    # mean_cost_util_w = np.mean(n_cost_util_w)
    # mean_cost_tran_w = np.mean(n_cost_tran_w)

    return wall_cost+damage_loss_w+inop_util_w+inop_tran_w+cost_util_w+cost_tran_w, wall_cost, df_cost_direct_sum_div_w, fld_h_w_sect_g, fld_h_w
