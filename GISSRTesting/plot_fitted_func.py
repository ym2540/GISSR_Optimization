import glob
import numpy as np
import pandas as pd

import params

from fun_setup import generate_sv
from fun_floodestimate import func_fit

######### Initialize Sections and Surface Volume Functions #########
SVf1, SVf2, SVf3, SVf4, SVf5, SVf6, SVf7, SVf8, SVf9, SVf10, SVf11, SVf12, SVf13, SVf14, SVf15, SVf16, SVf17, SVf18, SVf19, SVf20, SVfg1, SVfg2, SVfg3, SVfg4, SVfg5, SVfg6, SVfg7, SVfg8, SVfg9, SVfg10, SVfg11, SVfg12, SVfg13, SVfg14, SVfg15, SVfg16, SVfg17, SVfg18, SVfg19, SVfg20, SV_all = generate_sv()

n = 20

######### Evaluate all fitted functions
files = glob.glob(params.sv_combined_files)
data = np.ones(shape=(n * 20, len(files) * 2))
for div, f in enumerate(files):
    surfaceV_file = pd.read_csv(f)
    surfaceV = surfaceV_file["volume"]
    data_div = np.zeros((n * (len(surfaceV) - 1), 2))
    for vol_idx in range(surfaceV.size - 1):
        start = surfaceV[vol_idx]
        end = surfaceV[vol_idx + 1]
        for sub_vol_idx, vol in enumerate(np.linspace(start, end, num=n, endpoint=False)):
            if vol_idx == 0:    # there is no SVf0 for some reason!
                vol_idx = 1
            expr = "SVf" + str(vol_idx)
            SVf = eval(expr)
            a = SVf[div][0]
            b = SVf[div][1]
            height = func_fit(vol, a, b)
            data_div[vol_idx * n + sub_vol_idx, :] = [vol, height]
    data[:, [div*2, div*2 + 1]] = data_div

data_df = pd.DataFrame(data)
data_df.to_csv("fitted_surfaceV.csv")
