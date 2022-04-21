divs_allocate = [0,1,2,3,4,5]  # divs to allocate wall
h_start = 0.8  # startin height
h_end = 1.1  # ending height

dh = 0.0025

l_seg = 100  # length of a segment
dt = 1 * 60 ** 2  # length of a time segment in seconds
travel_dist = 2  # number of adjacent divisions (in one direction) that water can be redistributed to 

topo_file = "ideal_topo_1.csv"
storm_file = "SurgeData/0-surge_w.csv"
time_file = "SurgeData/0-time_w.csv"
div_data_file = "ideal_div_data.csv"