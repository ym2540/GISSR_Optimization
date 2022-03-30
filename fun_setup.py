import numpy as np
import pandas as pd
import glob

import params
from fun_floodestimate import SurfaceVolFunc


def generate_sv():
    ndiv18 = params.ndiv18
    files = glob.glob(params.sv_combined_files)
    groupcsvfiles = glob.glob(params.sv_grouped_files)
    H = np.append(np.linspace(0, 3, 13), np.linspace(3.5, 7, 8))

    SVfg1 = np.zeros([ndiv18, 2])
    SVfg2 = np.zeros([ndiv18, 2])
    SVfg3 = np.zeros([ndiv18, 2])
    SVfg4 = np.zeros([ndiv18, 2])
    SVfg5 = np.zeros([ndiv18, 2])
    SVfg6 = np.zeros([ndiv18, 2])
    SVfg7 = np.zeros([ndiv18, 2])
    SVfg8 = np.zeros([ndiv18, 2])
    SVfg9 = np.zeros([ndiv18, 2])
    SVfg10 = np.zeros([ndiv18, 2])
    SVfg11 = np.zeros([ndiv18, 2])
    SVfg12 = np.zeros([ndiv18, 2])
    SVfg13 = np.zeros([ndiv18, 2])
    SVfg14 = np.zeros([ndiv18, 2])
    SVfg15 = np.zeros([ndiv18, 2])
    SVfg16 = np.zeros([ndiv18, 2])
    SVfg17 = np.zeros([ndiv18, 2])
    SVfg18 = np.zeros([ndiv18, 2])
    SVfg19 = np.zeros([ndiv18, 2])
    SVfg20 = np.zeros([ndiv18, 2])

    i = 0
    for f in groupcsvfiles:
        surfaceVg = pd.read_csv(f)["volume"]
        SVfg1[i, :], SVfg2[i, :], SVfg3[i, :], SVfg4[i, :], SVfg5[i, :], SVfg6[i, :], SVfg7[i, :], SVfg8[i, :], SVfg9[i, :], SVfg10[i, :], SVfg11[i, :], SVfg12[i,
                                                                                                                                                                :], SVfg13[i, :], SVfg14[i, :], SVfg15[i, :], SVfg16[i, :], SVfg17[i, :], SVfg18[i, :], SVfg19[i, :], SVfg20[i, :] = SurfaceVolFunc(surfaceVg, H)
        i = i + 1

    SVf1 = np.zeros([ndiv18, 2])
    SVf2 = np.zeros([ndiv18, 2])
    SVf3 = np.zeros([ndiv18, 2])
    SVf4 = np.zeros([ndiv18, 2])
    SVf5 = np.zeros([ndiv18, 2])
    SVf6 = np.zeros([ndiv18, 2])
    SVf7 = np.zeros([ndiv18, 2])
    SVf8 = np.zeros([ndiv18, 2])
    SVf9 = np.zeros([ndiv18, 2])
    SVf10 = np.zeros([ndiv18, 2])
    SVf11 = np.zeros([ndiv18, 2])
    SVf12 = np.zeros([ndiv18, 2])
    SVf13 = np.zeros([ndiv18, 2])
    SVf14 = np.zeros([ndiv18, 2])
    SVf15 = np.zeros([ndiv18, 2])
    SVf16 = np.zeros([ndiv18, 2])
    SVf17 = np.zeros([ndiv18, 2])
    SVf18 = np.zeros([ndiv18, 2])
    SVf19 = np.zeros([ndiv18, 2])
    SVf20 = np.zeros([ndiv18, 2])

    SV_all = []
    i = 0
    for f in files:
        surfaceV_height = pd.read_csv(f)
        surfaceV = surfaceV_height["volume"]
        SV_all = np.append(SV_all, surfaceV)
        SVf1[i, :], SVf2[i, :], SVf3[i, :], SVf4[i, :], SVf5[i, :], SVf6[i, :], SVf7[i, :], SVf8[i, :], SVf9[i, :], SVf10[i, :], SVf11[i, :], SVf12[i,
                                                                                                                                                    :], SVf13[i, :], SVf14[i, :], SVf15[i, :], SVf16[i, :], SVf17[i, :], SVf18[i, :], SVf19[i, :], SVf20[i, :] = SurfaceVolFunc(surfaceV, H)
        i = i+1
    SV_all = SV_all.reshape(18, 21)

    return SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all


def generate_div_connections():
    sections = params.sections
    sect3 = np.zeros([len(sections)-6, 7])
    k = 3
    for i in sections[3:-3]:
        sect3[k-3] = [sections[k-3], sections[k-2], sections[k-1],
                      i, sections[k+1], sections[k+2], sections[k+3]]
        k = k + 1

    sect0 = [sections[0], sections[1], sections[2], sections[3]]
    sect1 = [sections[0], sections[1], sections[2], sections[3], sections[4]]
    sect2 = [sections[0], sections[1], sections[2],
             sections[3], sections[4], sections[5]]

    sect_3 = [sections[-6], sections[-5], sections[-4],
              sections[-3], sections[-2], sections[-1]]
    sect_2 = [sections[-5], sections[-4],
              sections[-3], sections[-2], sections[-1]]
    sect_1 = [sections[-4], sections[-3], sections[-2], sections[-1]]

    return sect0, sect1, sect2, sect3, sect_1, sect_2, sect_3
