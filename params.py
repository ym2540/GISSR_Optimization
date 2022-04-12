dh = 0.25  # delta height
budget = 3*10**9

storm_type = 'w'  # cold 'c' or warm 'w' 

ndiv18 = 18
sections = [10, 11, 5, 12, 1, 13, 16, 4, 17, 15, 3, 14, 0, 9, 8, 7, 2, 6]  # sections, ordered from north-east and clockwise
segment_l = 100  # length of a wall segment
nt = 24 # split number of time history of storm surge

sv_combined_files = r'NewSurfaceVolumeCombined/LMN_div18_*.csv'
sv_grouped_files = r'NewSurfaceVolumeGrouped/LMN_div18_*.csv'
roughness_file = "Roughness.csv"
slope_file = "LMN_Slope.csv"
wall_positions_file = r"BigU_LES_all.csv"
sandy_surge_file = r"CO-OPS_8518750_met_hr.csv"
topo_file = "LMN_div.csv"
pluto_file = "LMN_pluto_Div.csv"
fragility_file = "fragilitycurves.csv"

##### CONSTANTS #####
ftm = 0.3048  # ft to m
g = 9.80665  # gravity