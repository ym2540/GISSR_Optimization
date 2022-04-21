from damage import Damage
import numpy as np
import pandas as pd

pluto_file = "LMN_pluto_Div.csv"
fragility_file = "fragilitycurves.csv"

ftm = 0.3048  # ft to m

Damage = Damage(pluto_file, fragility_file)

data = []


water_level = np.zeros((1,18))
for i, h in enumerate(np.linspace(0, 5, num=100)):
    water_level[:] = h
    damage_loss_w, inop_util_w, inop_tran_w, cost_util_w, cost_tran_w, df_cost_direct_sum_div_w = Damage.dmg_cost_vector(water_level/ftm)
    data.append([h, *(df_cost_direct_sum_div_w["dirct_cost"].to_list())])

data_df = pd.DataFrame(data)
data_df.to_csv("damage_table.csv")