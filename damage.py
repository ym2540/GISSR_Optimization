
import numpy as np
import pandas as pd
import params
import numpy as np
import pandas as pd
#import csv
#import matplotlib.pyplot as plt
#import time

class Damage:
    def __init__(self, pluto_file="LMN_pluto_Div.csv", fragility_file="fragilitycurves.csv"):
        self.H_dmg = np.linspace(-4, 24, 29)
        self.H_dmg1 = np.linspace(0, 10, 11)

        self.pluto = pd.read_csv(pluto_file)
        self.df_curves = pd.read_csv(fragility_file)

        self.fid = self.pluto["FID"]
        self.crtcl_elv = self.pluto["MIN"]
        self.bldgasst = self.pluto["BldgAsst"]
        self.bsmt = self.pluto["BsmtCode"]
        self.comarea = self.pluto["ComArea"]
        self.fldpln = self.pluto["100yrFlood"]
        self.numfl = self.pluto["NumFloors"]
        self.bldgclass = self.pluto["BldgClass"]
        self.div = self.pluto["Div"]
        self.flh = 10  # floor height in ft

        # Critical Facilities
        self.df_fire = self.df_curves["fire"]
        self.df_poli = self.df_curves["poli"]
        self.df_hosp = self.df_curves["hosp"]
        self.df_nurs = self.df_curves["nurs"]
        self.df_schl = self.df_curves["schl"]
        self.df_eoc = self.df_curves["eoc"]
        self.df_res11 = self.df_curves["res11"]
        self.df_res11b = self.df_curves["res11b"]
        self.df_res12 = self.df_curves["res12"]
        self.df_res12b = self.df_curves["res12b"]
        self.df_res2 = self.df_curves["res2"]
        self.df_res3 = self.df_curves["res3"]
        self.df_res3b = self.df_curves["res3b"]
        self.df_htl = self.df_curves["htl"]
        self.df_com1 = self.df_curves["com1"]
        self.df_com2 = self.df_curves["com2"]
        self.df_com3 = self.df_curves["com3"]
        self.df_com4 = self.df_curves["com4"]
        self.df_com5 = self.df_curves["com5"]
        self.df_com7 = self.df_curves["com7"]
        self.df_com8 = self.df_curves["com8"]
        self.df_com9 = self.df_curves["com9"]
        self.df_com10 = self.df_curves["com10"]
        self.df_ind1 = self.df_curves["ind1"]
        self.df_ind2 = self.df_curves["ind2"]
        self.df_ind3 = self.df_curves["ind3"]
        self.df_ind4 = self.df_curves["ind4"]
        self.df_ind5 = self.df_curves["ind5"]
        self.df_ind6 = self.df_curves["ind6"]
        self.df_agr = self.df_curves["agr"]
        self.df_rel = self.df_curves["rel"]
        self.df_gov = self.df_curves["gov"]
        self.df_elec = self.df_curves['elec'][0:11]
        self.df_subs = self.df_curves['subs'][0:11]
    
    def dmg_cost_vector(self, fld_h):
        
        # start_time1 = time.time()
        
        flh = self.flh; fid = self.fid; crtcl_elv = self.crtcl_elv
        bldgasst = self.bldgasst; bsmt = self.bsmt; comarea = self.comarea
        fldpln = self.fldpln; numfl = self.numfl; bldgclass = self.bldgclass
        div = self.div; df_fire = self.df_fire; df_poli = self.df_poli
        df_hosp = self.df_hosp; df_nurs = self.df_nurs; df_schl = self.df_schl
        df_eoc = self.df_eoc; df_res11 = self.df_res11; df_res11b = self.df_res11b
        df_res12 = self.df_res12; df_res12b = self.df_res12b; df_res2 = self.df_res2
        df_res3 = self.df_res3; df_res3b = self.df_res3b; df_htl = self.df_htl
        df_com1 = self.df_com1; df_com2 = self.df_com2; df_com3 = self.df_com3
        df_com4 = self.df_com4; df_com5 = self.df_com5; df_com7 = self.df_com7
        df_com8 = self.df_com8; df_com9 = self.df_com9; df_com10 = self.df_com10
        df_ind1 = self.df_ind1; df_ind2 = self.df_ind2; df_ind3 = self.df_ind3
        df_ind4 = self.df_ind4; df_ind5 = self.df_ind5; df_ind6 = self.df_ind6
        df_agr = self.df_agr; df_rel = self.df_rel; df_gov = self.df_gov
        df_elec = self.df_elec; H = self.H_dmg; H1 = self.H_dmg1
        ftm = params.ftm

        damage_loss   = np.zeros((fld_h.shape[0],18))
        int_inop_util = np.zeros((fld_h.shape[0],13))
        int_inop_tran = np.zeros((fld_h.shape[0],13))
        int_cost_util = np.zeros((fld_h.shape[0],13))
        int_cost_tran = np.zeros((fld_h.shape[0],13))
        
        # setup        
        cost_dmg = np.zeros((fld_h.shape[0],fid.size)) # physical loss
        cost_inv = np.zeros((fld_h.shape[0],fid.size)) # inventory loss
        cost_inc = np.zeros((fld_h.shape[0],fid.size)) # income loss
        dmgp     = np.zeros((fld_h.shape[0],fid.size))
        dmgcost  = []
        
        # Damage Percentage      
        fire     = fid[bldgclass=='Y1']
        div_fire = div[fire]
        fldh_v   = -1.0*np.tile(crtcl_elv[fire],(fld_h.shape[0],1)) + fld_h[:,div_fire]
        dmgp[:,fire]     = np.interp(fldh_v, H, df_fire)
        dmgp[dmgp<0]=0
        cost_dmg[:,fire] = np.tile(bldgasst[fire],(fld_h.shape[0],1)) * dmgp[:,fire] / 100

        poli     = fid[bldgclass=='Y2']
        div_poli = div[poli]
        fldh_v   = -1.0*np.tile(crtcl_elv[poli],(fld_h.shape[0],1)) + fld_h[:,div_poli]
        dmgp[:,poli]     = np.interp(fldh_v, H, df_poli)
        dmgp[dmgp<0]=0
        cost_dmg[:,poli] = np.tile(bldgasst[poli],(fld_h.shape[0],1)) * dmgp[:,poli] / 100
        
        hosp     = fid[bldgclass=='I1']
        div_hosp = div[hosp]
        fldh_v   = - 1.0*np.tile(crtcl_elv[hosp],(fld_h.shape[0],1)) + fld_h[:,div_hosp]
        dmgp[:,hosp]     = np.interp(fldh_v, H, df_hosp)       # damage percent of total hospital
        dmgp[dmgp<0]=0
        cost_dmg[:,hosp] = np.tile(bldgasst[hosp],(fld_h.shape[0],1)) * dmgp[:,hosp] / 100
        d_hosp = np.zeros(fldh_v.shape)
        d_hosp[(-8 <= fldh_v)|(fldh_v < -4)] = 180
        d_hosp[(-4 <= fldh_v)|(fldh_v <  0)] = 360
        d_hosp[(0  <= fldh_v)|(fldh_v <  4)] = 540
        d_hosp[(4  <= fldh_v)|(fldh_v <  8)] = 720
        cost_inc[:,hosp] = (1-0.6) * np.tile(comarea[hosp],(fld_h.shape[0],1)) * dmgp[:,hosp] / 100 * 0.16 * d_hosp
            
        nurs     = fid[(bldgclass=='I6')|(bldgclass=='N1')|(bldgclass=='N2')|(bldgclass=='N3')|(bldgclass=='N4')|(bldgclass=='N9')]
        div_nurs = div[nurs]
        fldh_v   = -1.0*np.tile(crtcl_elv[nurs],(fld_h.shape[0],1)) + fld_h[:,div_nurs]             # flood height top
        dmgp[:,nurs] = np.interp(fldh_v, H, df_nurs)       # damage percent of total nursing home
        dmgp[dmgp<0]=0
        cost_dmg[:,nurs] = np.tile(bldgasst[nurs],(fld_h.shape[0],1)) * dmgp[:,nurs] / 100
        d_nurs = np.zeros(fldh_v.shape)
        d_nurs[np.tile(fldpln[nurs]==0,(fld_h.shape[0],1))] = 360
        d_nurs[np.tile(fldpln[nurs]==1,(fld_h.shape[0],1))] = 540
        d_nurs[(0  <= fldh_v)|(fldh_v <  4)] = 240
        d_nurs[(4  <= fldh_v)|(fldh_v <  8)] = 375
        d_nurs[(8  <= fldh_v)|(fldh_v <  12)] = 570
        cost_inc[:,nurs] = (1-0.6) * np.tile(comarea[nurs],(fld_h.shape[0],1)) * dmgp[:,nurs] / 100 * 0.16 * d_nurs
            
        schl = fid[(bldgclass=='W1')|(bldgclass=='W2')|(bldgclass=='W3')|(bldgclass=='W4')|(bldgclass=='W5')|(bldgclass=='W6')|(bldgclass=='W7')|(bldgclass=='W8')|(bldgclass=='W9')]
        div_schl = div[schl]
        fldh_v = -1.0*np.tile(crtcl_elv[schl],(fld_h.shape[0],1)) + fld_h[:,div_schl]
        dmgp[:,schl] = np.interp(fldh_v, H, df_schl)       # damage percent of total schools
        dmgp[dmgp<0]=0
        cost_dmg[:,schl] = np.tile(bldgasst[schl],(fld_h.shape[0],1)) * dmgp[:,schl] / 100
        d_schl = np.zeros(fldh_v.shape)
        d_schl[np.tile(fldpln[schl]==0,(fld_h.shape[0],1))] = 360
        d_schl[np.tile(fldpln[schl]==1,(fld_h.shape[0],1))] = 540
        d_schl[(0  <= fldh_v)|(fldh_v <  4)] = 240
        d_schl[(4  <= fldh_v)|(fldh_v <  8)] = 375
        d_schl[(8  <= fldh_v)|(fldh_v <  12)] = 570    
        cost_inc[:,schl] = (1-0.6) * np.tile(comarea[schl],(fld_h.shape[0],1)) * dmgp[:,schl] / 100 * 0.245 * d_schl
            
        com1 = fid[(bldgclass=='K1')|(bldgclass=='K2')|(bldgclass=='K3')|(bldgclass=='K4')|(bldgclass=='K5')|(bldgclass=='K6')|(bldgclass=='K8')|(bldgclass=='K9')|(bldgclass=='RC')]
        div_com1 = div[com1]
        fldh_v = -1.0*np.tile(crtcl_elv[com1],(fld_h.shape[0],1)) + fld_h[:,div_com1]
        dmgp[:,com1[numfl[com1]< 7]] = np.interp(fldh_v[:,numfl[com1]<7], H, df_com1)
        dmgp[:,com1[numfl[com1]>=7]] = fldh_v[:,numfl[com1]>=7] / flh / np.tile(numfl[com1[numfl[com1]>=7]],(fld_h.shape[0],1)) * 100
        dmgp[dmgp<0]=0
        cost_dmg[:,com1] = np.tile(bldgasst[com1],(fld_h.shape[0],1)) * dmgp[:,com1] / 100
        cost_inv[:,com1] = dmgp[:,com1] / 100 * np.tile(comarea[com1],(fld_h.shape[0],1)) * 46 * 0.13
        d_com1 = np.zeros(fldh_v.shape)
        d_com1[np.tile(fldpln[com1]==0,(fld_h.shape[0],1))] = 360
        d_com1[np.tile(fldpln[com1]==1,(fld_h.shape[0],1))] = 540
        d_com1[(0 <= fldh_v)|(fldh_v <  4)] = 300
        d_com1[(4 <= fldh_v)|(fldh_v <  8)] = 480
        d_com1[(8 <= fldh_v)|(fldh_v < 12)] = 750
        cost_inc[:,com1] = (1-0.87) * np.tile(comarea[com1],(fld_h.shape[0],1)) * dmgp[:,com1] / 100 * 0.06 * d_com1

        com2 = fid[(bldgclass=='E1')|(bldgclass=='E2')|(bldgclass=='E3')|(bldgclass=='E4')|(bldgclass=='E7')|(bldgclass=='E9')|(bldgclass=='RI')|(bldgclass=='RW')]
        div_com2 = div[com2]
        fldh_v = -1.0*np.tile(crtcl_elv[com2],(fld_h.shape[0],1)) + fld_h[:,div_com2]
        dmgp[:,com2] = np.interp(fldh_v, H, df_com2) #Wholesale Damage
        dmgp[dmgp<0]=0
        cost_dmg[:,com2] = np.tile(bldgasst[com2],(fld_h.shape[0],1)) * dmgp[:,com2] / 100
        cost_inv[:,com2] = dmgp[:,com2] / 100 * np.tile(comarea[com2],(fld_h.shape[0],1)) * 66 * 0.1
        d_com2 = np.zeros(fldh_v.shape)
        d_com2[np.tile(fldpln[com2]==0,(fld_h.shape[0],1))] = 360
        d_com2[np.tile(fldpln[com2]==1,(fld_h.shape[0],1))] = 540
        d_com2[(0  <= fldh_v)|(fldh_v <  4)] = 300
        d_com2[(4  <= fldh_v)|(fldh_v <  8)] = 480
        d_com2[(8  <= fldh_v)|(fldh_v <  12)] = 750  
        cost_inc[:,com2] = (1-0.87) * np.tile(comarea[com2],(fld_h.shape[0],1)) * dmgp[:,com2] / 100 * 0.1 * d_com2
            
        com4     = fid[(bldgclass=='O1')|(bldgclass=='O2')|(bldgclass=='O3')|(bldgclass=='O4')|(bldgclass=='O5')|(bldgclass=='O6')|(bldgclass=='O7')|(bldgclass=='O8')|(bldgclass=='O9')|(bldgclass=='RB')]
        div_com4 = div[com4]
        fldh_v   = -1.0*np.tile(crtcl_elv[com4],(fld_h.shape[0],1)) + fld_h[:,div_com4]
        dmgp[:,com4[numfl[com4]< 7]] = np.interp(fldh_v[:,numfl[com4]<7], H, df_com4)
        dmgp[:,com4[numfl[com4]>=7]] = fldh_v[:,numfl[com4]>=7] / flh / np.tile(numfl[com4[numfl[com4]>=7]],(fld_h.shape[0],1)) * 100
        dmgp[dmgp<0]=0
        cost_dmg[:,com4] = np.tile(bldgasst[com4],(fld_h.shape[0],1)) * dmgp[:,com4] / 100
        d_com4 = np.zeros(fldh_v.shape)
        d_com4[np.tile(fldpln[com4]==0,(fld_h.shape[0],1))] = 360
        d_com4[np.tile(fldpln[com4]==1,(fld_h.shape[0],1))] = 540
        d_com4[(0 <= fldh_v)|(fldh_v <  4)] = 240
        d_com4[(4 <= fldh_v)|(fldh_v <  8)] = 375
        d_com4[(8 <= fldh_v)|(fldh_v < 12)] = 570
        cost_inc[:,com4] = (1-0.9) * np.tile(comarea[com4],(fld_h.shape[0],1)) * dmgp[:,com4] / 100 * 1.03 * d_com4
            
        com5     = fid[bldgclass=='K7']
        div_com5 = div[com5]
        fldh_v   = -1.0*np.tile(crtcl_elv[com5],(fld_h.shape[0],1)) + fld_h[:,div_com5]
        dmgp[:,com5[numfl[com5]< 7]] = np.interp(fldh_v[:,numfl[com5]<7], H, df_com5)
        dmgp[:,com5[numfl[com5]>=7]] = fldh_v[:,numfl[com5]>=7] / flh / np.tile(numfl[com5[numfl[com5]>=7]],(fld_h.shape[0],1)) * 100
        dmgp[dmgp<0]=0
        cost_dmg[:,com5] = np.tile(bldgasst[com5],(fld_h.shape[0],1)) * dmgp[:,com5] / 100
        d_com5 = np.zeros(fldh_v.shape)
        d_com5[np.tile(fldpln[com5]==0,(fld_h.shape[0],1))] = 360
        d_com5[np.tile(fldpln[com5]==1,(fld_h.shape[0],1))] = 540
        d_com5[(0 <= fldh_v)|(fldh_v <  4)] = 240
        d_com5[(4 <= fldh_v)|(fldh_v <  8)] = 375
        d_com5[(8 <= fldh_v)|(fldh_v < 12)] = 570
        cost_inc[:,com5] = (1-0.9) * np.tile(comarea[com5],(fld_h.shape[0],1)) * dmgp[:,com5] / 100 * 1.18 * d_com5
        
        com7     = fid[(bldgclass=='I2')|(bldgclass=='I3')|(bldgclass=='I4')|(bldgclass=='I5')|(bldgclass=='I7')|(bldgclass=='I9')]
        div_com7 = div[com7]
        fldh_v   = -1.0*np.tile(crtcl_elv[com7],(fld_h.shape[0],1)) + fld_h[:,div_com7]
        dmgp[:,com7] = np.interp(fldh_v, H, df_com7)       # damage percent of total Medical Office
        dmgp[dmgp<0]=0
        cost_dmg[:,com7] = np.tile(bldgasst[com7],(fld_h.shape[0],1)) * dmgp[:,com7] / 100
        d_com7 = np.zeros(fldh_v.shape)
        d_com7[np.tile(fldpln[com7]==0,(fld_h.shape[0],1))] = 360
        d_com7[np.tile(fldpln[com7]==1,(fld_h.shape[0],1))] = 540
        d_com7[(0 <= fldh_v)|(fldh_v <  4)] = 240
        d_com7[(4 <= fldh_v)|(fldh_v <  8)] = 375
        d_com7[(8 <= fldh_v)|(fldh_v < 12)] = 570 
        cost_inc[:,com7] = (1-0.6) * np.tile(comarea[com7],(fld_h.shape[0],1)) * dmgp[:,com7] / 100 * 0.33 * d_com7
        
        com8     = fid[(bldgclass=='P3')|(bldgclass=='P4')|(bldgclass=='P5')|(bldgclass=='P6')|(bldgclass=='P7')|(bldgclass=='P8')|(bldgclass=='P9')|(bldgclass=='Q1')|(bldgclass=='Q2')|(bldgclass=='Q3')|(bldgclass=='Q4')|(bldgclass=='Q5')|(bldgclass=='Q6')|(bldgclass=='Q7')|(bldgclass=='Q8')|(bldgclass=='Q9')|(bldgclass=='RA')]
        div_com8 = div[com8]
        fldh_v   = -1.0*np.tile(crtcl_elv[com8],(fld_h.shape[0],1)) + fld_h[:,div_com8]
        dmgp[:,com8] = np.interp(fldh_v, H, df_com8)       # damage percent of total Entertainment and Recreation
        dmgp[dmgp<0]=0
        cost_dmg[:,com8] = np.tile(bldgasst[com8],(fld_h.shape[0],1)) * dmgp[:,com8] / 100
        d_com8 = np.zeros(fldh_v.shape)
        d_com8[np.tile(fldpln[com8]==0,(fld_h.shape[0],1))] = 360
        d_com8[np.tile(fldpln[com8]==1,(fld_h.shape[0],1))] = 540
        d_com8[(0  <= fldh_v)|(fldh_v <  4)]  = 300
        d_com8[(4  <= fldh_v)|(fldh_v <  8)]  = 480
        d_com8[(8  <= fldh_v)|(fldh_v <  12)] = 750      
        cost_inc[:,com8] = (1-0.6) * np.tile(comarea[com8],(fld_h.shape[0],1)) * dmgp[:,com8] / 100 * 0.6 * d_com8
        
        com9     = fid[(bldgclass=='P1')|(bldgclass=='J1')|(bldgclass=='J2')|(bldgclass=='J3')|(bldgclass=='J4')|(bldgclass=='J5')|(bldgclass=='J6')|(bldgclass=='J7')|(bldgclass=='J8')|(bldgclass=='J9')]
        div_com9 = div[com9]
        fldh_v   = -1.0*np.tile(crtcl_elv[com9],(fld_h.shape[0],1)) + fld_h[:,div_com9]
        dmgp[:,com9] = np.interp(fldh_v, H, df_com9)       # damage percent of total theater
        dmgp[dmgp<0]=0
        cost_dmg[:,com9] = np.tile(bldgasst[com9],(fld_h.shape[0],1)) * dmgp[:,com9] / 100
        d_com9 = np.zeros(fldh_v.shape)
        d_com9[np.tile(fldpln[com9]==0,(fld_h.shape[0],1))] = 360
        d_com9[np.tile(fldpln[com9]==1,(fld_h.shape[0],1))] = 540
        d_com9[(0  <= fldh_v)|(fldh_v <  4)] = 300
        d_com9[(4  <= fldh_v)|(fldh_v <  8)] = 480
        d_com9[(8  <= fldh_v)|(fldh_v <  12)] = 750
        cost_inc[:,com9] = (1-0.6) * np.tile(comarea[com9],(fld_h.shape[0],1)) * dmgp[:,com9] / 100 * 0.2 * d_com9
        
        #added to building class for com10 T2, T9, U7, U1
        com10     = fid[(bldgclass=='G0')|(bldgclass=='G1')|(bldgclass=='G2')|(bldgclass=='G3')|(bldgclass=='G4')|(bldgclass=='G5')|(bldgclass=='G6')|(bldgclass=='G7')|(bldgclass=='G8')|(bldgclass=='G9')|(bldgclass=='GU')|(bldgclass=='GW')|(bldgclass=='RP')|(bldgclass=='RG')|(bldgclass=='U1')|(bldgclass=='T9')|(bldgclass=='T2')|(bldgclass=='U7')]
        div_com10 = div[com10]
        fldh_v    = -1.0*np.tile(crtcl_elv[com10],(fld_h.shape[0],1)) + fld_h[:,div_com10]
        dmgp[:,com10] = np.interp(fldh_v, H, df_com10)       # damage percent of total Parking
        dmgp[dmgp<0]=0
        cost_dmg[:,com10] = np.tile(bldgasst[com10],(fld_h.shape[0],1)) * dmgp[:,com10] / 100
        d_com10 = np.zeros(fldh_v.shape)
        d_com10[0 < fldh_v] = 30
        cost_inc[:,com10] = (1-0.6) * np.tile(comarea[com10],(fld_h.shape[0],1)) * dmgp[:,com10] / 100 * 0 * d_com10
    
        ind1     = fid[bldgclass=='F1']
        div_ind1 = div[ind1]
        fldh_v   = -1.0*np.tile(crtcl_elv[ind1],(fld_h.shape[0],1)) + fld_h[:,div_ind1]
        dmgp[:,ind1] = np.interp(fldh_v, H, df_ind1)       # damage percent of total heavy industrial 
        dmgp[dmgp<0]=0
        cost_dmg[:,ind1] = np.tile(bldgasst[ind1],(fld_h.shape[0],1)) * dmgp[:,ind1] / 100
        cost_inv[:,ind1] = dmgp[:,ind1] / 100 * np.tile(comarea[ind1],(fld_h.shape[0],1)) * 616 * 0.05
        d_ind1 = np.zeros(fldh_v.shape)
        d_ind1[0 < fldh_v] = 60
        cost_inc[:,ind1] = (1-0.98) * np.tile(comarea[ind1],(fld_h.shape[0],1)) * dmgp[:,ind1] / 100 * 0.25 * d_ind1        
    
        ind2     = fid[(bldgclass=='F4')|(bldgclass=='F5')|(bldgclass=='F8')|(bldgclass=='F9')]
        div_ind2 = div[ind2]
        fldh_v   = -1.0*np.tile(crtcl_elv[ind2],(fld_h.shape[0],1)) + fld_h[:,div_ind2]
        dmgp[:,ind2] = np.interp(fldh_v, H, df_ind2)       # damage percent of total light industrial 
        dmgp[dmgp<0]=0
        cost_dmg[:,ind2] = np.tile(bldgasst[ind2],(fld_h.shape[0],1)) * dmgp[:,ind2] / 100  
        cost_inv[:,ind2] = dmgp[:,ind2] / 100 * np.tile(comarea[ind2],(fld_h.shape[0],1)) * 196 * 0.04
        d_ind2 = np.zeros(fldh_v.shape)
        d_ind2[0 < fldh_v] = 45
        cost_inc[:,ind2] = (1-0.98) * np.tile(comarea[ind2],(fld_h.shape[0],1)) * dmgp[:,ind2] / 100 * 0.25 * d_ind2
        
        ind6 = fid[bldgclass=='F2']
        div_ind6 = div[ind6]
        fldh_v = -1.0*np.tile(crtcl_elv[ind6],(fld_h.shape[0],1)) + fld_h[:,div_ind6]
        dmgp[:,ind6] = np.interp(fldh_v, H, df_ind6)   
        dmgp[dmgp<0]=0
        cost_dmg[:,ind6] = np.tile(bldgasst[ind6],(fld_h.shape[0],1)) * dmgp[:,ind6] / 100
        cost_inv[:,ind6] = dmgp[:,ind6] / 100 * np.tile(comarea[ind6],(fld_h.shape[0],1)) * 664* 0.02
        d_ind6 = np.zeros(fldh_v.shape)
        d_ind6[0 < fldh_v] = 45
        cost_inc[:,ind6] = (1-0.95) * np.tile(comarea[ind6],(fld_h.shape[0],1)) * dmgp[:,ind6] / 100 * 0.24 * d_ind6
        
        rel = fid[(bldgclass=='M1')|(bldgclass=='M2')|(bldgclass=='M3')|(bldgclass=='M4')|(bldgclass=='M9')]
        div_rel = div[rel]
        fldh_v = -1.0*np.tile(crtcl_elv[rel],(fld_h.shape[0],1)) + fld_h[:,div_rel]
        dmgp[:,rel] = np.interp(fldh_v, H, df_rel)       # damage percent of total religious building 
        dmgp[dmgp<0]=0
        cost_dmg[:,rel] = np.tile(bldgasst[rel],(fld_h.shape[0],1)) * dmgp[:,rel] / 100
        d_rel = np.zeros(fldh_v.shape)
        d_rel[np.tile(fldpln[rel]==0,(fld_h.shape[0],1))] = 360
        d_rel[np.tile(fldpln[rel]==1,(fld_h.shape[0],1))] = 540
        d_rel[(0  <= fldh_v)|(fldh_v <  4)] = 300
        d_rel[(4  <= fldh_v)|(fldh_v <  8)] = 480
        d_rel[(8  <= fldh_v)|(fldh_v < 12)] = 750       
        cost_inc[:,rel] = (1-0.6) * np.tile(comarea[rel],(fld_h.shape[0],1)) * dmgp[:,rel] / 100 * 0.13 * d_rel
    
        gov = fid[(bldgclass=='Y3')|(bldgclass=='Y4')|(bldgclass=='Y5')|(bldgclass=='Y6')|(bldgclass=='Y7')|(bldgclass=='Y8')|(bldgclass=='Y9')]
        div_gov = div[gov]
        fldh_v = -1.0*np.tile(crtcl_elv[gov],(fld_h.shape[0],1)) + fld_h[:,div_gov]
        dmgp[:,gov] = np.interp(fldh_v, H, df_gov)# damage percent of total government
        dmgp[dmgp<0]=0
        cost_dmg[:,gov] = np.tile(bldgasst[gov],(fld_h.shape[0],1)) * dmgp[:,gov] / 100
        d_gov = np.zeros(fldh_v.shape)
        d_gov[np.tile(fldpln[gov]==0,(fld_h.shape[0],1))] = 360
        d_gov[np.tile(fldpln[gov]==1,(fld_h.shape[0],1))] = 540
        d_gov[(0 <= fldh_v)|(fldh_v <  4)] = 240
        d_gov[(4 <= fldh_v)|(fldh_v <  8)] = 375
        d_gov[(8 <= fldh_v)|(fldh_v < 12)] = 570
        cost_inc[:,gov] = (1-0.8) * np.tile(comarea[gov],(fld_h.shape[0],1)) * dmgp[:,gov] / 100 * 0.11 * d_gov
        
        #elec = fid[(bldgclass=='U0')|(bldgclass=='U2')|(bldgclass=='U3')|(bldgclass=='U4')|(bldgclass=='U5')|(bldgclass=='U9')]
        elec = fid[(bldgclass=='U0')|(bldgclass=='U2')|(bldgclass=='U4')|(bldgclass=='U9')]
        div_elec = div[elec]
        fldh_v = -1.0*np.tile(crtcl_elv[elec],(fld_h.shape[0],1)) + fld_h[:,div_elec]
        dmgp[:,elec] = np.interp(fldh_v, H1, df_elec)       # damage percent of total electric
        dmgp[dmgp<0]=0
        cost_dmg[:,elec] = (np.tile(bldgasst[elec],(fld_h.shape[0],1)) * dmgp[:,elec]) / 100      
            
        htl = fid[(bldgclass=='H1')|(bldgclass=='H2')|(bldgclass=='H3')|(bldgclass=='H4')|(bldgclass=='H5')|(bldgclass=='H6')|(bldgclass=='H7')|(bldgclass=='H8')|(bldgclass=='H9')|(bldgclass=='HB')|(bldgclass=='HH')|(bldgclass=='HR')|(bldgclass=='HS')|(bldgclass=='RH')|(bldgclass=='P2')]
        div_htl = div[htl]
        fldh_v = -1.0*np.tile(crtcl_elv[htl],(fld_h.shape[0],1)) + fld_h[:,div_htl]
        dmgp[:,htl[numfl[htl]< 7]] = np.interp(fldh_v[:,numfl[htl]<7], H, df_htl)
        dmgp[:,htl[numfl[htl]>=7]] = fldh_v[:,numfl[htl]>=7] / flh / np.tile(numfl[htl[numfl[htl]>=7]],(fld_h.shape[0],1)) * 100
        dmgp[dmgp<0]=0
        cost_dmg[:,htl] = np.tile(bldgasst[htl],(fld_h.shape[0],1)) * dmgp[:,htl] / 100 
        d_htl = np.zeros(fldh_v.shape)
        d_htl[np.tile(fldpln[htl]==0,(fld_h.shape[0],1))] = 360
        d_htl[np.tile(fldpln[htl]==1,(fld_h.shape[0],1))] = 540
        d_htl[(0 <= fldh_v)|(fldh_v <  4)] = 195
        d_htl[(4 <= fldh_v)|(fldh_v <  8)] = 300
        d_htl[(8 <= fldh_v)|(fldh_v < 12)] = 360
        cost_inc[:,htl] = (1-0.6) * np.tile(comarea[htl],(fld_h.shape[0],1)) * dmgp[:,htl] / 100 * 0.1 * d_htl

        res11 = fid[(bldgclass=='A0')|(bldgclass=='A2')|(bldgclass=='A3')|(bldgclass=='A5')|(bldgclass=='A6')|(bldgclass=='A8')]
        res11a = res11[bsmt==0] # no basement
        res11b = res11[bsmt!=0] # basement
        div_res11a = div[res11a]
        div_res11b = div[res11b]
        fldh11_a = -1.0*np.tile(crtcl_elv[res11a],(fld_h.shape[0],1)) + fld_h[:,div_res11a]
        fldh11_b = -1.0*np.tile(crtcl_elv[res11b],(fld_h.shape[0],1)) + fld_h[:,div_res11b]
        dmgp[:,res11a] = np.interp(fldh11_a, H, df_res11)
        dmgp[:,res11b] = np.interp(fldh11_b, H, df_res11b)
        dmgp[dmgp<0]=0
        cost_dmg[:,res11a] = np.tile(bldgasst[res11a],(fld_h.shape[0],1)) * dmgp[:,res11a] / 100
        cost_dmg[:,res11b] = np.tile(bldgasst[res11b],(fld_h.shape[0],1)) * dmgp[:,res11b] / 100
        
        res12 = fid[(bldgclass=='A1')|(bldgclass=='A4')|(bldgclass=='A7')|(bldgclass=='S0')|(bldgclass=='S1')]
        res12a = res12[bsmt==0] # no basement
        res12b = res12[bsmt!=0] # basement
        div_res12a = div[res12a]
        div_res12b = div[res12b]
        fldh12_a = -1.0*np.tile(crtcl_elv[res12a],(fld_h.shape[0],1)) + fld_h[:,div_res12a]
        fldh12_b = -1.0*np.tile(crtcl_elv[res12b],(fld_h.shape[0],1)) + fld_h[:,div_res12b]
        dmgp[:,res12a] = np.interp(fldh12_a, H, df_res12)
        dmgp[:,res12b] = np.interp(fldh12_b, H, df_res12b)
        dmgp[dmgp<0]=0
        cost_dmg[:,res12a] = np.tile(bldgasst[res12a],(fld_h.shape[0],1)) * dmgp[:,res12a] / 100
        cost_dmg[:,res12b] = np.tile(bldgasst[res12b],(fld_h.shape[0],1)) * dmgp[:,res12b] / 100

        res3a = fid[((bldgclass=='B1')|(bldgclass=='B2')|(bldgclass=='B3')|(bldgclass=='B9')|(bldgclass=='S2')|(bldgclass=='S3')|(bldgclass=='S4')|(bldgclass=='S5')|(bldgclass=='S9')|(bldgclass=='R0')|(bldgclass=='R1')|(bldgclass=='R2')|(bldgclass=='R3')|(bldgclass=='R4')|(bldgclass=='R5')|(bldgclass=='R6')|(bldgclass=='R7')|(bldgclass=='R8')|(bldgclass=='R9')|(bldgclass=='RD')|(bldgclass=='RR')|(bldgclass=='RS')|(bldgclass=='RT')|(bldgclass=='RZ')|(bldgclass=='RX')|(bldgclass=='RM'))&(bsmt==0)]
        res3b = fid[((bldgclass=='B1')|(bldgclass=='B2')|(bldgclass=='B3')|(bldgclass=='B9')|(bldgclass=='S2')|(bldgclass=='S3')|(bldgclass=='S4')|(bldgclass=='S5')|(bldgclass=='S9')|(bldgclass=='R0')|(bldgclass=='R1')|(bldgclass=='R2')|(bldgclass=='R3')|(bldgclass=='R4')|(bldgclass=='R5')|(bldgclass=='R6')|(bldgclass=='R7')|(bldgclass=='R8')|(bldgclass=='R9')|(bldgclass=='RD')|(bldgclass=='RR')|(bldgclass=='RS')|(bldgclass=='RT')|(bldgclass=='RZ')|(bldgclass=='RX')|(bldgclass=='RM'))&(bsmt!=0)]
        div_res3a = div[res3a]
        div_res3b = div[res3b]
        fldh3_a = -1.0*np.tile(crtcl_elv[res3a],(fld_h.shape[0],1)) + fld_h[:,div_res3a]
        fldh3_b = -1.0*np.tile(crtcl_elv[res3b],(fld_h.shape[0],1)) + fld_h[:,div_res3b]
        dmgp[:,res3a[numfl[res3a]< 7]] = np.interp(fldh3_a[:,numfl[res3a]<7], H, df_res3)
        dmgp[:,res3b[numfl[res3b]< 7]] = np.interp(fldh3_b[:,numfl[res3b]<7], H, df_res3b)
        dmgp[:,res3a[numfl[res3a]>=7]] = fldh3_a[:,numfl[res3a]>=7] / flh / np.tile(numfl[res3a[numfl[res3a]>=7]],(fld_h.shape[0],1)) * 100
        dmgp[:,res3b[numfl[res3b]>=7]] = fldh3_b[:,numfl[res3b]>=7] / flh / np.tile(numfl[res3b[numfl[res3b]>=7]],(fld_h.shape[0],1)) * 100
        dmgp[dmgp<0]=0
        cost_dmg[:,res3a] = np.tile(bldgasst[res3a],(fld_h.shape[0],1)) * dmgp[:,res3a] / 100
        cost_dmg[:,res3b] = np.tile(bldgasst[res3b],(fld_h.shape[0],1)) * dmgp[:,res3b] / 100
        
        ###########################################
        
        ### newly added on Nov 9, 2021 for getting total damage in each division
        
        cost_dmg_inc_inc   = np.column_stack((np.sum(cost_dmg,axis=0),np.sum(cost_inc,axis=0),np.sum(cost_inv,axis=0))) # matrix of costs for each building
        cost_direct        = np.sum(cost_dmg_inc_inc,axis=1) # sum of direct damage for each building
        df_cost_direct_div = pd.DataFrame({'dirct_cost':cost_direct,'DIV':div}) 
        df_cost_direct_sum_div = df_cost_direct_div.groupby(by=["DIV"]).sum()
        
        
        ##below is the code to find the percentage of damage to each sector
        dmg_elec  = np.mean(dmgp[:,elec],  axis=1)
        dmg_com10 = np.mean(dmgp[:,com10], axis=1)

        #below the total damage costt is calculated for all the sectors except for electricity 
        elec_l  = np.sum(cost_dmg[:,elec], axis=1)
        hosp_l  = np.sum(cost_dmg[:,hosp], axis=1) + np.sum(cost_inc[:,hosp], axis=1)      
        poli_l  = np.sum(cost_dmg[:,poli], axis=1)                
        nurs_l  = np.sum(cost_dmg[:,nurs], axis=1) + np.sum(cost_inc[:,nurs], axis=1)        
        com1_l  = np.sum(cost_dmg[:,com1], axis=1) + np.sum(cost_inc[:,com1], axis=1) + np.sum(cost_inc[:,com1], axis=1)      
        com2_l  = np.sum(cost_dmg[:,com2], axis=1) + np.sum(cost_inc[:,com2], axis=1) + np.sum(cost_inc[:,com2], axis=1)      
        com4_l  = np.sum(cost_dmg[:,com4], axis=1) + np.sum(cost_inc[:,com4], axis=1)
        com5_l  = np.sum(cost_dmg[:,com5], axis=1) + np.sum(cost_inc[:,com5], axis=1)       
        com7_l  = np.sum(cost_dmg[:,com7], axis=1) + np.sum(cost_inc[:,com7], axis=1)
        com8_l  = np.sum(cost_dmg[:,com8], axis=1) + np.sum(cost_inc[:,com8], axis=1)
        com9_l  = np.sum(cost_dmg[:,com9], axis=1) + np.sum(cost_inc[:,com9], axis=1)
        com10_l = np.sum(cost_dmg[:,com10], axis=1) + np.sum(cost_inc[:,com10], axis=1)
        ind1_l  = np.sum(cost_dmg[:,ind1], axis=1) + np.sum(cost_inc[:,ind1], axis=1) + np.sum(cost_inc[:,ind1], axis=1)
        ind2_l  = np.sum(cost_dmg[:,ind2], axis=1) + np.sum(cost_inc[:,ind2], axis=1) + np.sum(cost_inc[:,ind2], axis=1)
        ind6_l  = np.sum(cost_inc[:,ind6], axis=1) + np.sum(cost_inv[:,ind6], axis=1) + np.sum(cost_dmg[:,ind6], axis=1)
        rel_l   = np.sum(cost_dmg[:,rel],  axis=1) + np.sum(cost_inc[:,rel],  axis=1)
        gov_l   = np.sum(cost_dmg[:,gov],  axis=1) + np.sum(cost_inc[:,gov],  axis=1)
        fire_l  = np.sum(cost_dmg[:,fire], axis=1)
        res11_l = np.sum(cost_dmg[:,res11a], axis=1) + np.sum(cost_dmg[:,res11b], axis=1)
        res12_l = np.sum(cost_dmg[:,res12a], axis=1) + np.sum(cost_dmg[:,res12b], axis=1)
        res3_l  = np.sum(cost_dmg[:,res3a],  axis=1) + np.sum(cost_dmg[:,res3b],  axis=1)
        htl_l   = np.sum(cost_dmg[:,htl],    axis=1) + np.sum(cost_inc[:,htl],    axis=1)
        res_l   = res11_l + res12_l + res3_l 
        ttl_l   = res11_l + res12_l + res3_l + gov_l + fire_l + nurs_l + hosp_l + com1_l + com2_l + com4_l + com5_l + com7_l + com8_l + com9_l + com10_l + ind1_l + ind2_l + rel_l
               
        damage_loss = np.column_stack((res11_l,res12_l,res3_l,gov_l,fire_l,nurs_l,hosp_l,com1_l,com2_l,com4_l,com5_l,com7_l,com8_l,com9_l,com10_l,ind1_l,ind2_l,rel_l))


        ## Inoperability
        tran_inop=np.zeros((fld_h.shape[0],));   tran_cost=np.zeros((fld_h.shape[0],));   crit_inop=np.zeros((fld_h.shape[0],));  crit_cost=np.zeros((fld_h.shape[0],))
        comm_inop=np.zeros((fld_h.shape[0],));   comm_cost=np.zeros((fld_h.shape[0],));   wtr_inop=np.zeros((fld_h.shape[0],));   wtr_cost=np.zeros((fld_h.shape[0],))
        fin_inop=np.zeros((fld_h.shape[0],));    fin_cost=np.zeros((fld_h.shape[0],));    util_inop=np.zeros((fld_h.shape[0],));  util_cost=np.zeros((fld_h.shape[0],))
        gov_inop=np.zeros((fld_h.shape[0],));    gov_cost=np.zeros((fld_h.shape[0],));    emerg_inop=np.zeros((fld_h.shape[0],)); emerg_cost=np.zeros((fld_h.shape[0],))
        fuel_inop=np.zeros((fld_h.shape[0],));   fuel_cost=np.zeros((fld_h.shape[0],));   com_inop=np.zeros((fld_h.shape[0],));   com_cost=np.zeros((fld_h.shape[0],))
        build_inop=np.zeros((fld_h.shape[0],));  build_cost=np.zeros((fld_h.shape[0],));  food_inop=np.zeros((fld_h.shape[0],));  food_cost=np.zeros((fld_h.shape[0],))
        health_inop=np.zeros((fld_h.shape[0],)); health_cost=np.zeros((fld_h.shape[0],)); inter_inop=np.zeros((fld_h.shape[0],)); inter_cost=np.zeros((fld_h.shape[0],))

        # if dmg_elec > 0:#the code below finds the inoperability percentages for the critical infrastructture sectors in the Crupi, Agrawal, Cimerallo paper
        tran_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .164
        tran_cost[dmg_elec>0] = tran_inop[dmg_elec>0]/100 * com10_l[dmg_elec>0]
        crit_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .046 #* ((dmg_ind1 + dmg_ind2)/2)
        crit_cost[dmg_elec>0] = crit_inop[dmg_elec>0]/100  * (ind1_l[dmg_elec>0] + ind2_l[dmg_elec>0])
        comm_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .0323 #* ((dmg_com4 + dmg_com1 + dmg_com2)/3)
        comm_cost[dmg_elec>0] = comm_inop[dmg_elec>0]/100 * (com4_l[dmg_elec>0] + com1_l[dmg_elec>0] + com2_l[dmg_elec>0])
        wtr_inop[dmg_elec>0]  = dmg_elec[dmg_elec>0] * .054 #* ((dmg_res + dmg_nurs + dmg_com4 + dmg_com7 + dmg_com8 + dmg_com9 + dmg_fire + dmg_poli + dmg_com1 + dmg_com2 + dmg_gov)/11)
        wtr_cost[dmg_elec>0]  = wtr_inop[dmg_elec>0]/100 * (res_l[dmg_elec>0] + nurs_l[dmg_elec>0] + com4_l[dmg_elec>0] + com7_l[dmg_elec>0] + com8_l[dmg_elec>0] + com9_l[dmg_elec>0] + fire_l[dmg_elec>0] + poli_l[dmg_elec>0] + com1_l[dmg_elec>0] + com2_l[dmg_elec>0] + gov_l[dmg_elec>0])
        fin_inop[dmg_elec>0]  = dmg_elec[dmg_elec>0] * .019 #* dmg_com5
        fin_cost[dmg_elec>0]  = fin_inop[dmg_elec>0]/100 * com5_l[dmg_elec>0]
        util_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * 1
        util_cost[dmg_elec>0] = util_inop[dmg_elec>0]/100 * ttl_l[dmg_elec>0]
        gov_inop[dmg_elec>0]  = dmg_elec[dmg_elec>0] * .009 #* dmg_gov 
        gov_cost[dmg_elec>0]  = gov_inop[dmg_elec>0]/100 * gov_l[dmg_elec>0]
        emerg_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .012 #* ((dmg_poli + dmg_fire)/2)
        emerg_cost[dmg_elec>0] = emerg_inop[dmg_elec>0]/100 * (poli_l[dmg_elec>0] + fire_l[dmg_elec>0])
        fuel_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .587
        fuel_cost[dmg_elec>0] = fuel_inop[dmg_elec>0]/100 * ttl_l[dmg_elec>0]
        com_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .015 #* ((dmg_res + dmg_nurs + dmg_com4 + dmg_com5 + dmg_ind2 + dmg_ind1 + dmg_com7 + dmg_com8 + dmg_com9 + dmg_fire + dmg_poli + dmg_com1 + dmg_com2 + dmg_gov)/14)
        com_cost[dmg_elec>0] = com_inop[dmg_elec>0]/100 * (res_l[dmg_elec>0] + nurs_l[dmg_elec>0] + com4_l[dmg_elec>0] + com5_l[dmg_elec>0] + ind2_l[dmg_elec>0] + ind1_l[dmg_elec>0] + com7_l[dmg_elec>0] + com8_l[dmg_elec>0] + com9_l[dmg_elec>0] + fire_l[dmg_elec>0] + poli_l[dmg_elec>0] + com1_l[dmg_elec>0] + com2_l[dmg_elec>0] + gov_l[dmg_elec>0])
        build_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .06 #* dmg_res
        build_cost[dmg_elec>0] = build_inop[dmg_elec>0]/100 * res_l[dmg_elec>0]
        food_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .002 #* ((dmg_res + dmg_com8 + dmg_com1 + dmg_com2)/4)
        food_cost[dmg_elec>0] = food_inop[dmg_elec>0]/100 * (res_l[dmg_elec>0] + com8_l[dmg_elec>0] + com1_l[dmg_elec>0] + com2_l[dmg_elec>0])          
        health_inop[dmg_elec>0] = dmg_elec[dmg_elec>0] * .15 #* ((dmg_hosp + dmg_nurs + dmg_com7)/3)
        health_cost[dmg_elec>0] = health_inop[dmg_elec>0]/100 * (hosp_l[dmg_elec>0] + nurs_l[dmg_elec>0] + com7_l[dmg_elec>0])
        inter_cost[dmg_elec>0] = tran_cost[dmg_elec>0] + crit_cost[dmg_elec>0] + comm_cost[dmg_elec>0] + com_cost[dmg_elec>0] + util_cost[dmg_elec>0] + wtr_cost[dmg_elec>0] + fin_cost[dmg_elec>0]+ gov_cost[dmg_elec>0] + emerg_cost[dmg_elec>0] + fuel_cost[dmg_elec>0] + food_cost[dmg_elec>0] + health_cost[dmg_elec>0]
        inter_inop[dmg_elec>0] = (tran_inop[dmg_elec>0] + emerg_inop[dmg_elec>0] + health_inop[dmg_elec>0]+ food_inop[dmg_elec>0]+ build_inop[dmg_elec>0]+ com_inop[dmg_elec>0]+ comm_inop[dmg_elec>0]+ wtr_inop[dmg_elec>0] + util_inop[dmg_elec>0]+ fin_inop[dmg_elec>0] + emerg_inop[dmg_elec>0]+ fuel_inop[dmg_elec>0]+ gov_inop[dmg_elec>0])/13

        tran_tinop=np.zeros((fld_h.shape[0],));   tran_tcost=np.zeros((fld_h.shape[0],));   crit_tinop=np.zeros((fld_h.shape[0],));  crit_tcost=np.zeros((fld_h.shape[0],))
        comm_tinop=np.zeros((fld_h.shape[0],));   comm_tcost=np.zeros((fld_h.shape[0],));   wtr_tinop=np.zeros((fld_h.shape[0],));   wtr_tcost=np.zeros((fld_h.shape[0],))
        fin_tinop=np.zeros((fld_h.shape[0],));    fin_tcost=np.zeros((fld_h.shape[0],));    util_tinop=np.zeros((fld_h.shape[0],));  util_tcost=np.zeros((fld_h.shape[0],))
        gov_tinop=np.zeros((fld_h.shape[0],));    gov_tcost=np.zeros((fld_h.shape[0],));    emerg_tinop=np.zeros((fld_h.shape[0],)); emerg_tcost=np.zeros((fld_h.shape[0],))
        fuel_tinop=np.zeros((fld_h.shape[0],));   fuel_tcost=np.zeros((fld_h.shape[0],));   com_tinop=np.zeros((fld_h.shape[0],));   com_tcost=np.zeros((fld_h.shape[0],))
        build_tinop=np.zeros((fld_h.shape[0],));  build_tcost=np.zeros((fld_h.shape[0],));  food_tinop=np.zeros((fld_h.shape[0],));  food_tcost=np.zeros((fld_h.shape[0],))
        health_tinop=np.zeros((fld_h.shape[0],)); health_tcost=np.zeros((fld_h.shape[0],)); inter_tinop=np.zeros((fld_h.shape[0],)); inter_tcost=np.zeros((fld_h.shape[0],))

        # if dmg_com10 > 0:#the code below finds the inoperability percentages for the critical infrastructture sectors in the Crupi, Agrawal, Cimerallo paper
        tran_tinop[dmg_com10>0] = dmg_com10[dmg_com10>0]
        tran_tcost[dmg_com10>0] = (tran_tinop[dmg_com10>0]/100) * (com10_l[dmg_com10>0] + fire_l[dmg_com10>0] + poli_l[dmg_com10>0])
        crit_tinop[dmg_com10>0] = dmg_com10[dmg_com10>0] * .236
        crit_tcost[dmg_com10>0] = (crit_tinop[dmg_com10>0]/100)  * (ind1_l[dmg_com10>0] + ind2_l[dmg_com10>0])
        comm_tinop[dmg_com10>0] = dmg_com10[dmg_com10>0] * .168
        comm_tcost[dmg_com10>0] = (comm_tinop[dmg_com10>0]/100) * (com4_l[dmg_com10>0] + com1_l[dmg_com10>0] + com2_l[dmg_com10>0])
        wtr_tinop[dmg_com10>0]  = dmg_com10[dmg_com10>0] * .129
        wtr_tcost[dmg_com10>0]  = (wtr_tinop[dmg_com10>0]/100) * (res_l[dmg_com10>0] + nurs_l[dmg_com10>0] + com4_l[dmg_com10>0] + com7_l[dmg_com10>0] + com8_l[dmg_com10>0] + com9_l[dmg_com10>0] + fire_l[dmg_com10>0] + poli_l[dmg_com10>0] + com1_l[dmg_com10>0] + com2_l[dmg_com10>0] + gov_l[dmg_com10>0])
        fin_tinop[dmg_com10>0]  = (dmg_com10[dmg_com10>0] * .109) #* dmg_com5
        fin_tcost[dmg_com10>0]  = (fin_tinop[dmg_com10>0]/100) * com5_l[dmg_com10>0]
        util_tinop[dmg_com10>0] = (dmg_com10[dmg_com10>0] * .093)
        util_tcost[dmg_com10>0] = (util_tinop[dmg_com10>0]/100) * ttl_l[dmg_com10>0]
        gov_tinop[dmg_com10>0]  = (dmg_com10[dmg_com10>0] * .084) #* dmg_gov 
        gov_tcost[dmg_com10>0]  = (gov_tinop[dmg_com10>0]/100) * gov_l[dmg_com10>0]
        emerg_tinop[dmg_com10>0] = (dmg_com10[dmg_com10>0] * .049) #* ((dmg_poli + dmg_fire)/2)
        emerg_tcost[dmg_com10>0] = (emerg_tinop[dmg_com10>0]/100) * (poli_l[dmg_com10>0] + fire_l[dmg_com10>0])
        fuel_tinop[dmg_com10>0]  = dmg_com10[dmg_com10>0] * .049
        fuel_tcost[dmg_com10>0]  = (fuel_tinop[dmg_com10>0]/100) * ttl_l[dmg_com10>0]
        com_tinop[dmg_com10>0]   = (dmg_com10[dmg_com10>0] * .048) #* ((dmg_res + dmg_nurs + dmg_com4 + dmg_com5 + dmg_ind2 + dmg_ind1 + dmg_com7 + dmg_com8 + dmg_com9 + dmg_fire + dmg_poli + dmg_com1 + dmg_com2 + dmg_gov)/14)
        com_tcost[dmg_com10>0]   = (com_tinop[dmg_com10>0]/100) * (res_l[dmg_com10>0] + nurs_l[dmg_com10>0] + com4_l[dmg_com10>0] + com5_l[dmg_com10>0] + ind2_l[dmg_com10>0] + ind1_l[dmg_com10>0] + com7_l[dmg_com10>0] + com8_l[dmg_com10>0] + com9_l[dmg_com10>0] + fire_l[dmg_com10>0] + poli_l[dmg_com10>0] + com1_l[dmg_com10>0] + com2_l[dmg_com10>0] + gov_l[dmg_com10>0])
        build_tinop[dmg_com10>0] = (dmg_com10[dmg_com10>0] * .03) #* dmg_res
        build_tcost[dmg_com10>0] = (build_tinop[dmg_com10>0]/100) * res_l[dmg_com10>0]
        food_tinop[dmg_com10>0]  = (dmg_com10[dmg_com10>0] * .006) #* ((dmg_res + dmg_com8 + dmg_com1 + dmg_com2)/4)
        food_tcost[dmg_com10>0]  = (food_tinop[dmg_com10>0]/100) * (res_l[dmg_com10>0] + com8_l[dmg_com10>0] + com1_l[dmg_com10>0] + com2_l[dmg_com10>0])          
        health_tinop[dmg_com10>0] = (dmg_com10[dmg_com10>0] * .05) #* ((dmg_hosp + dmg_nurs + dmg_com7)/3)
        health_tcost[dmg_com10>0] = (health_tinop[dmg_com10>0]/100) * (hosp_l[dmg_com10>0] + nurs_l[dmg_com10>0] + com7_l[dmg_com10>0])
        inter_tinop[dmg_com10>0] = (tran_tinop[dmg_com10>0] + emerg_tinop[dmg_com10>0] + health_tinop[dmg_com10>0]+ food_tinop[dmg_com10>0]+ build_tinop[dmg_com10>0]+ com_tinop[dmg_com10>0]+ comm_tinop[dmg_com10>0]+ wtr_tinop[dmg_com10>0] + util_tinop[dmg_com10>0]+ fin_tinop[dmg_com10>0] + emerg_tinop[dmg_com10>0]+ fuel_tinop[dmg_com10>0]+ gov_tinop[dmg_com10>0])/13
        inter_tcost[dmg_com10>0] = tran_tcost[dmg_com10>0] + crit_tcost[dmg_com10>0] + comm_tcost[dmg_com10>0] + com_tcost[dmg_com10>0] + util_tcost[dmg_com10>0] + wtr_tcost[dmg_com10>0] + fin_tcost[dmg_com10>0] + gov_tcost[dmg_com10>0] + emerg_tcost[dmg_com10>0] + fuel_tcost[dmg_com10>0] + food_tcost[dmg_com10>0] + health_tcost[dmg_com10>0]

        int_inop_util = np.column_stack((tran_inop,crit_inop,comm_inop,wtr_inop,fin_inop,util_inop,gov_inop,emerg_inop,fuel_inop,com_inop,build_inop,food_inop,health_inop))
        int_inop_tran = np.column_stack((tran_tinop,crit_tinop,comm_tinop,wtr_tinop,fin_tinop,util_tinop,gov_tinop,emerg_tinop,fuel_tinop,com_tinop,build_tinop,food_tinop,health_tinop))
        int_cost_util = np.column_stack((tran_cost,crit_cost,comm_cost,wtr_cost,fin_cost,util_cost,gov_cost,emerg_cost,fuel_cost,com_cost,build_cost,food_cost,health_cost))
        int_cost_tran = np.column_stack((tran_tcost,crit_tcost,comm_tcost,wtr_tcost,fin_tcost,util_tcost,gov_tcost,emerg_tcost,fuel_tcost,com_tcost,build_tcost,food_tcost,health_tcost))
        
        damage_loss = np.sum(damage_loss,axis=1)
        int_inop_util = np.sum(int_inop_util,axis=1)
        int_inop_tran = np.sum(int_inop_tran,axis=1)
        int_cost_util = np.sum(int_cost_util,axis=1)
        int_cost_tran = np.sum(int_cost_tran,axis=1)
        
        return damage_loss,int_inop_util,int_inop_tran,int_cost_util,int_cost_tran, df_cost_direct_sum_div
