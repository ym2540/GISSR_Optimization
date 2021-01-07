# # -*- coding: utf-8 -*-
# """
# Created on Thu Aug 13 11:01:37 2020

# @author: Yuki
# """

import numpy as np
import scipy as sp
import pandas as pd
import time
import glob                                                                                                      
import datetime

## import functions
from fun_floodestimate          import FloodHeight
from fun_floodestimate          import FloodHeightWall
from fun_floodestimate          import FloodTravelSectGroup
from fun_floodestimate          import SurfaceVolFunc
from fun_damagecost             import damage
from fun_SubwayFlood_noPrtc_opt import storm_econ_loss


def objective(x,SVf1,SVf2,SVf3,SVf4,SVf5,SVf6,SVf7,SVf8,SVf9,SVf10,SVf11,SVf12,SVf13,SVf14,SVf15,SVf16,SVf17,SVf18,SVf19,SVf20,
                SVfg1,SVfg2,SVfg3,SVfg4,SVfg5,SVfg6,SVfg7,SVfg8,SVfg9,SVfg10,SVfg11,SVfg12,SVfg13,SVfg14,SVfg15,SVfg16,SVfg17,SVfg18,SVfg19,SVfg20,
                SV_all,roughness,slope,sect0,sect1,sect2,sect3,sect_1,sect_2,sect_3):
    
    ftm = 0.3048
    nt = 10

    # wall info
    # wall_id = pd.read_csv("C:\\Users\\Yuki\\Documents\\Research\\ArcGIS\\GeoData\\Segments\\BigU\\BigU_LES_all.csv")["ID"]
    wall_h   = x[0]
    wall_year = x[1]
    wall_start = x[2]
    wall_end  = x[3]
    wall_num    = np.arange(int(wall_start),int(wall_end-wall_start)) # need to refer position and fid: fid[position == wall_id]

    # wall_cost = (22195*wall_h-16553)*wall_id.size*100/((1+0.05)**(wall_year-2020))
    # wall_cost = (22195*wall_h-16553)*(wall_end-wall_start)*100/((1+0.05)**(wall_year-2020))
    wall_cost = 109360*wall_h*(wall_end-wall_start)*100

    # num_N = 1000

    # Topography Data
    topo = pd.read_csv("LMN_div.csv")
    elev = topo["MEAN"]
    fid  = topo["FID"]
    div18 = topo["DIV18"]
    position = topo["POSITION"]  
    ndiv18 = np.unique(div18).size
    l = 100
    #sandy_surge = pd.read_csv("C:\\Users\\Yuki\\Documents\\Research\\Flood Volume\\20121029_CO-OPS_8518750_wl.csv")
    #surge_height = sandy_surge["Surge"]

    wall_id  = fid[(position>=wall_start) & (position<=wall_end)]

    ###################### Subway Setup ######################

    ## Import Subway Data
    SubwayOpenings = pd.read_csv(r"SubwayData\AllOpenings_LMN_fill.csv")

    Vulnerabil = SubwayOpenings["Vulnerabil"];    Mitigation = SubwayOpenings["Mitigation"]
    Mitigati_1 = SubwayOpenings["Mitigati_1"];    CrtclElev  = SubwayOpenings["Crtcl_Elev"]
    SubwayLineName = SubwayOpenings["LINE"];      fid_open   = SubwayOpenings["OBJECTID"]
    division   = SubwayOpenings["Div"]
    assigned_line = SubwayOpenings['Line_FID']

    OpenArea = np.zeros(fid_open.size)
    OpenArea[Vulnerabil == 'Door']           = 7.33*3.33*ftm**2;    OpenArea[Vulnerabil == 'Elevator']       = 9.08*8.5*ftm**2
    OpenArea[Vulnerabil == 'Emergency Exit'] = 7.33*3.33*ftm**2;    OpenArea[Vulnerabil == 'Escalator']      = 9.08*8.5*ftm**2
    OpenArea[Vulnerabil == 'Hatch']          = 7.33*3.33*ftm**2;    OpenArea[Vulnerabil == 'Louver']         = 9.08*8.5*ftm**2
    OpenArea[Vulnerabil == 'Door']           = 7.33*3.33*ftm**2;    OpenArea[Vulnerabil == 'Manhole']        = 9.08*8.5*ftm**2
    OpenArea[Vulnerabil == 'Stairway']       = 7.33*3.33*ftm**2;    OpenArea[Vulnerabil == 'Vault']          = 9.08*8.5*ftm**2
    OpenArea[Vulnerabil == 'Vent Battery']   = 9.08*8.5*ftm**2;     OpenArea[Mitigation == 'Deployable cover'] = OpenArea[Mitigation == 'Deployable cover']*0.8

    LeakRate = np.zeros(fid_open.size)
    c = 0.134/ftm/60 # leakage rate (gallon/min/meter)
    LeakRate[Mitigation == 'Deployable cover'] = c;         LeakRate[Mitigation == 'Flex-gate'] = c
    LeakRate[Mitigation == 'MCD'] = 0.3*c;                  LeakRate[Mitigation == 'Removable flood panel'] = 0.1*c
    LeakRate[Mitigation == 'Stop logs'] = 0.1*c;            LeakRate[Mitigation == 'Watertight cover'] = 0.1*c
    LeakRate[Mitigation == 'Watertight hatch'] = 0.1*c;     LeakRate[Mitigation == 'Watertight/Marine door'] = 0.1*c

    # import subwayline data
    SubwayLine = pd.read_csv(r"SubwayData\SubwayLineConnect.csv")
    SubwayStop = pd.read_csv(r"SubwayData\SubwayStationLMN+Open.csv")

    fid_line = SubwayLine["FID"]
    fid_stop = SubwayStop["objectid"]
    exploc_stop = SubwayStop["ExpLoc"]
    length_line = SubwayLine["length_m"]
    elev_line = SubwayLine["MEAN"] - SubwayLine["STD"]
    elev_stop = SubwayStop["MEAN"]
    exploc_line = SubwayLine["ExpLoc"]
    tunelev_line = elev_line - 20*ftm
    tunelev_stop = elev_stop - 20*ftm
    div_line = SubwayLine["Div"]
    div_stop = SubwayStop["Div"]
    name_line = SubwayLine["name_text"]
    name_stop = SubwayStop["line_text"]
    StopOpening = SubwayStop["Open300m"] # openings within 300 m

    secarea_1trk = 15*30*ftm**2;    secarea_2trk = 15*30*ftm**2*2

    north_id = SubwayLine["North_FID"]
    south_id1 = SubwayLine["South_FID"];         south_id2      = SubwayLine["South_FID2"];    south_id3 = SubwayLine["South_FID3"]
    north_id_stop = SubwayLine["North_Stop"];    south_id_stop  = SubwayLine["South_Stop"]

    line_intersection = pd.read_csv(r"SubwayData\subwaystopscode.csv")
    elev_code = line_intersection["Elevation Code"].values
    station_complex = line_intersection["Station Complex"]
    div_subwaycode = line_intersection["Div"]

    ###################### Setup Surge Property ##############

    loc = 0.68;        ftm = 0.3048;       nt = 10;           g = 9.81
    xi_c = 0.08;       delta_c = 0.14;     lambda_c = 4.11
    xi_w = 0.45;       delta_w = 0.13;     lambda_w = 1.52
    beta1_1_c = 27.84; beta1_2_c = -18.58; beta2_1_c = 10.46; beta2_2_c = -6.98
    beta1_1_w = 19.23; beta1_2_w = -11.90; beta2_1_w = 4.96;  beta2_2_w = -1.89
    alpha_c = 3;       beta_c = 3.1;       alpha_w = 2.56;    beta_w = 2.07

    ###################### set up damage cost ################

    # other essentials
    g   = 9.80665  # gravity
    l   = 100       # span/length of each segment
    ftm = 0.3048 # ft to m
    H_dmg   = np.linspace(-4, 24, 29)
    H_dmg1  = np.linspace(0, 10, 11)

    pluto     = pd.read_csv("LMN_pluto_Div.csv")
    df_curves = pd.read_csv('fragilitycurves.csv')

    fid_dmg   = pluto["FID"]
    crtcl_elv = pluto["MIN"]
    bldgasst  = pluto["BldgAsst"]
    bsmt      = pluto["BsmtCode"]
    comarea   = pluto["ComArea"]
    fldpln    = pluto["100yrFlood"]
    numfl     = pluto["NumFloors"]
    bldgclass = pluto["BldgClass"]
    div       = pluto["Div"]
    flh       = 10 # floor height in ft

    # Critical Facilities
    df_fire = df_curves["fire"]; df_poli = df_curves["poli"]; df_hosp = df_curves["hosp"]
    df_nurs = df_curves["nurs"]; df_schl = df_curves["schl"]; df_eoc = df_curves["eoc"]
    df_res11 = df_curves["res11"]; df_res11b = df_curves["res11b"]; df_res12 = df_curves["res12"]
    df_res12b = df_curves["res12b"]; df_res2 = df_curves["res2"]; df_res3  = df_curves["res3"]
    df_res3b = df_curves["res3b"]; df_htl = df_curves["htl"]; df_com1 = df_curves["com1"]
    df_com2 = df_curves["com2"]; df_com3 = df_curves["com3"]; df_com4 = df_curves["com4"]
    df_com5 = df_curves["com5"]; df_com7 = df_curves["com7"]; df_com8 = df_curves["com8"]
    df_com9 = df_curves["com9"]; df_com10 = df_curves["com10"]; df_ind1 = df_curves["ind1"]
    df_ind2 = df_curves["ind2"]; df_ind3 = df_curves["ind3"]; df_ind4 = df_curves["ind4"]
    df_ind5 = df_curves["ind5"]; df_ind6 = df_curves["ind6"]; df_agr = df_curves["agr"]
    df_rel = df_curves["rel"]; df_gov = df_curves["gov"]; df_elec = df_curves['elec'][0:11]; df_subs = df_curves['subs'][0:11]


    ###################### MAIN #################################

    elev = topo["MEAN"]
    elev[wall_id] = elev[wall_id] + wall_h

    n_damage_loss_c = [];   n_damage_loss_w = []
    n_cost_util_c   = [];   n_cost_util_w   = []
    n_cost_tran_c   = [];   n_cost_tran_w   = []
    n_econ_subway_c = [];   n_econ_subway_w = []

    # start_time = time.time()

    for N in range(1):
        # flood estimation
        # numstorm = pd.read_csv(r"C:\Users\Yuki\Documents\Research\Python\2020 Flood Damage Loss\Optimization\SurgeData\%d-num_storm.csv"%N).values
        peak_c = pd.read_csv(r"C:\Users\Yuki\Documents\Research\Python\2020 Flood Damage Loss\Optimization\SurgeData\%d-peak_c.csv"%N).values
        peak_w = pd.read_csv(r"C:\Users\Yuki\Documents\Research\Python\2020 Flood Damage Loss\Optimization\SurgeData\%d-peak_w.csv"%N).values
        surge_c = pd.read_csv(r"C:\Users\Yuki\Documents\Research\Python\2020 Flood Damage Loss\Optimization\SurgeData\%d-surge_c.csv"%N).values
        surge_w = pd.read_csv(r"C:\Users\Yuki\Documents\Research\Python\2020 Flood Damage Loss\Optimization\SurgeData\%d-surge_w.csv"%N).values
        time_c = pd.read_csv(r"C:\Users\Yuki\Documents\Research\Python\2020 Flood Damage Loss\Optimization\SurgeData\%d-time_c.csv"%N).values
        time_w = pd.read_csv(r"C:\Users\Yuki\Documents\Research\Python\2020 Flood Damage Loss\Optimization\SurgeData\%d-time_w.csv"%N).values
        
        peak_c = peak_c.reshape((peak_c.size,))
        peak_w = peak_w.reshape((peak_w.size,))

        time1_c  = time_c[:,:10]
        time2_c  = time_c[:,10:]
        cpi1_c   = surge_c[:,:10]
        cpi2_c   = surge_c[:,10:]
        
        time1_w  = time_w[:,:10]
        time2_w  = time_w[:,10:]
        cpi1_w   = surge_w[:,:10]
        cpi2_w   = surge_w[:,10:]
        
        fld_h_c = np.zeros((np.shape(cpi1_c)[0],ndiv18)); fld_h_w = np.zeros((np.shape(cpi1_w)[0],ndiv18))
        V_c = np.zeros((np.shape(cpi1_c)[0],ndiv18)); V_w = np.zeros((np.shape(cpi1_w)[0],ndiv18))

        i = 0
        for i in range(18):
            fld_h_w[:,i],V_w[:,i] = FloodHeightWall(SV_all[i],wall_id,slope[i],roughness[i],SVf1[i,:],SVf2[i,:],SVf3[i,:],SVf4[i,:],SVf5[i,:],SVf6[i,:],SVf7[i,:],SVf8[i,:],SVf9[i,:],SVf10[i,:],SVf11[i,:],SVf12[i,:],SVf13[i,:],SVf14[i,:],SVf15[i,:],SVf16[i,:],SVf17[i,:],SVf18[i,:],SVf19[i,:],SVf20[i,:],time1_w,time2_w,cpi1_w,cpi2_w,nt,elev[div18==i],fid[div18==i],l,peak_w,i)
            fld_h_c[:,i],V_c[:,i] = FloodHeightWall(SV_all[i],wall_id,slope[i],roughness[i],SVf1[i,:],SVf2[i,:],SVf3[i,:],SVf4[i,:],SVf5[i,:],SVf6[i,:],SVf7[i,:],SVf8[i,:],SVf9[i,:],SVf10[i,:],SVf11[i,:],SVf12[i,:],SVf13[i,:],SVf14[i,:],SVf15[i,:],SVf16[i,:],SVf17[i,:],SVf18[i,:],SVf19[i,:],SVf20[i,:],time1_c,time2_c,cpi1_c,cpi2_c,nt,elev[div18==i],fid[div18==i],l,peak_c,i)

        # redistribution - group
        fld_h_w_sect_g,V_w_sect_avr = FloodTravelSectGroup(SV_all,ndiv18,peak_w,sect0,sect1,sect2,sect3,sect_3,sect_2,sect_1,V_w,SVfg1,SVfg2,SVfg3,SVfg4,SVfg5,SVfg6,SVfg7,SVfg8,SVfg9,SVfg10,SVfg11,SVfg12,SVfg13,SVfg14,SVfg15,SVfg16,SVfg17,SVfg18,SVfg19,SVfg20)
        fld_h_c_sect_g,V_c_sect_avr = FloodTravelSectGroup(SV_all,ndiv18,peak_c,sect0,sect1,sect2,sect3,sect_3,sect_2,sect_1,V_c,SVfg1,SVfg2,SVfg3,SVfg4,SVfg5,SVfg6,SVfg7,SVfg8,SVfg9,SVfg10,SVfg11,SVfg12,SVfg13,SVfg14,SVfg15,SVfg16,SVfg17,SVfg18,SVfg19,SVfg20)

        # Subway Flooding 
        loss_econ_list_c = []; days_pump_list_c = []; loss_econ_list_w = []; days_pump_list_w = []

        loss_econ_list_c,days_pump_list_c = storm_econ_loss(fld_h_c_sect_g,fid_line,fid_stop,exploc_stop, LeakRate, OpenArea, north_id, south_id1, south_id2,south_id3, 
                                                        north_id_stop, south_id_stop, elev_code, station_complex, div_subwaycode, elev_stop, exploc_line,tunelev_stop,
                                                        tunelev_line, div_line, div_stop, secarea_1trk, secarea_2trk,assigned_line, CrtclElev,fid_open, division,
                                                        beta1_1_c,beta1_2_c,beta2_1_c,beta2_2_c,alpha_c,beta_c,days_pump_list_c,loss_econ_list_c)
        loss_econ_list_w,days_pump_list_w = storm_econ_loss(fld_h_w_sect_g,fid_line,fid_stop,exploc_stop, LeakRate, OpenArea, north_id, south_id1, south_id2,south_id3, 
                                                        north_id_stop, south_id_stop, elev_code, station_complex, div_subwaycode, elev_stop, exploc_line,tunelev_stop,
                                                        tunelev_line, div_line, div_stop, secarea_1trk, secarea_2trk,assigned_line, CrtclElev,fid_open, division,
                                                        beta1_1_w,beta1_2_w,beta2_1_w,beta2_2_w,alpha_w,beta_w,days_pump_list_w,loss_econ_list_w)

        n_econ_subway_c = np.append(n_econ_subway_c,np.sum(loss_econ_list_c))
        n_econ_subway_w = np.append(n_econ_subway_w,np.sum(loss_econ_list_w))

        # damage analysis
        fld_h_c = fld_h_c_sect_g/ftm
        fld_h_w = fld_h_w_sect_g/ftm
        
        damage_loss_c,inop_util_c,inop_tran_c,cost_util_c,cost_tran_c  = damage.dmg_cost_vector(fld_h_c, flh, ftm, fid_dmg, crtcl_elv, bldgasst, bsmt, comarea, fldpln, numfl, bldgclass, div, df_fire, df_poli, df_hosp, df_nurs, df_schl, df_eoc, df_res11, df_res11b, df_res12, df_res12b, df_res2, df_res3, df_res3b, df_htl, df_com1, df_com2, df_com3, df_com4, df_com5, df_com7, df_com8, df_com9, df_com10, df_ind1, df_ind2, df_ind3, df_ind4, df_ind5, df_ind6, df_agr, df_rel, df_gov, df_elec,H_dmg,H_dmg1,N)
        damage_loss_w,inop_util_w,inop_tran_w,cost_util_w,cost_tran_w  = damage.dmg_cost_vector(fld_h_w, flh, ftm, fid_dmg, crtcl_elv, bldgasst, bsmt, comarea, fldpln, numfl, bldgclass, div, df_fire, df_poli, df_hosp, df_nurs, df_schl, df_eoc, df_res11, df_res11b, df_res12, df_res12b, df_res2, df_res3, df_res3b, df_htl, df_com1, df_com2, df_com3, df_com4, df_com5, df_com7, df_com8, df_com9, df_com10, df_ind1, df_ind2, df_ind3, df_ind4, df_ind5, df_ind6, df_agr, df_rel, df_gov, df_elec,H_dmg,H_dmg1,N)

        n_damage_loss_c = np.append(n_damage_loss_c,np.sum(damage_loss_c));   n_damage_loss_w = np.append(n_damage_loss_w,np.sum(damage_loss_w))
        n_cost_util_c   = np.append(n_cost_util_c,np.sum(cost_util_c));       n_cost_util_w   = np.append(n_cost_util_w,np.sum(inop_util_w))
        n_cost_tran_c   = np.append(n_cost_tran_c,np.sum(cost_tran_c));       n_cost_tran_w   = np.append(n_cost_tran_w,np.sum(cost_tran_w))



    mean_damage_loss_c  = np.mean(n_damage_loss_c); mean_damage_loss_w  = np.mean(n_damage_loss_w)
    mean_cost_util_c    = np.mean(n_cost_util_c);   mean_cost_util_w    = np.mean(n_cost_util_w)
    mean_cost_tran_c    = np.mean(n_cost_tran_c);   mean_cost_tran_w    = np.mean(n_cost_tran_w)
    mean_econ_subway_c  = np.mean(n_econ_subway_c); mean_econ_subway_w  = np.mean(n_econ_subway_w); 

    return wall_cost + mean_damage_loss_c + mean_damage_loss_w + mean_cost_util_c + mean_cost_util_w + mean_cost_tran_c + mean_cost_tran_w + mean_econ_subway_c + mean_econ_subway_w, wall_cost
