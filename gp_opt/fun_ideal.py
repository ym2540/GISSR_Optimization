# Author: Abel Valko
# Date: April 2022
#
# Functions to be used by subdivísion-redistribution inundation code
#


import numpy as np
import pandas as pd
import params_ideal as params

def get_wall_heights(Topo, min_height):
    wall_heights = min_height - Topo.shore_height_wall
    wall_heights[Topo.shore_height >= min_height] = 0
    positions = list(range(len(wall_heights)))
    return positions, wall_heights


def calc_flood_height(Topo, surge, surge_time, wall_height, wall_pos):
    r"""Calculates the first hand (direct) flood height and volume in each division given a surge, topography, and wall

    :Input:
    - *Topo* 
    - *surge*
    - *surge_time*
    - *wall_height*
    - *wall_pos*

    """

    h_crit = Topo.shore_height.copy()
    pos_nonzero = [pos for pos in wall_pos if wall_height[pos] > 0]  # Get indices of only non-zero height wall segment
    
    if pos_nonzero != []:

        foo = np.maximum(Topo.shore_height_wall[pos_nonzero] + wall_height[pos_nonzero], h_crit[pos_nonzero])
        h_crit[pos_nonzero] = np.maximum(Topo.shore_height_wall[pos_nonzero] + wall_height[pos_nonzero], h_crit[pos_nonzero])  # Set critical height to highest point at each segment, wall or not

    volume_div = np.zeros((surge.shape[0], Topo.divs.size))
    height_div = np.zeros((surge.shape[0], Topo.divs.size))
    #  Calculate direct inflow of water to each division
    for div in Topo.divs:

        vel = np.zeros(surge.shape)
        subsections_div = Topo.subsections[(Topo.all_divs == div)]  # all subsections of current division
        volume_sub = np.zeros((surge.shape[0], subsections_div.size))

        #  Each subdivision/subsection may have different height, but same slope and roughness
        for i, subsection in enumerate(subsections_div):

            h_diff = surge - np.ones(surge.shape) * h_crit[subsection] 
            vel[h_diff > 0] = ((params.l_seg * h_diff[h_diff > 0]) / (params.l_seg + 2 * h_diff[h_diff > 0])) ** (2/3) * Topo.slope_manning[div] ** (1/2) / Topo.roughness[div]  # Manning's equation for subdivision
            vel[h_diff < 0] = 0

            if wall_height[subsection] > 0:
                cwr = 0.611 + 0.075 * h_diff / np.tile(h_crit[subsection], surge.shape)  # Weir coeff if there is wall
                # if any(c > 1 for c in cwr.flatten()):
                #     print("Cwr over 1!!! Not good!")
                vel = vel * cwr
            volume_sub[:, i] = np.sum(params.l_seg * params.dt * h_diff * vel, axis=1)

        volume_div[:, div] = np.sum(volume_sub, axis=1)

        # Limit water level to surge peak (Likely not quite realistic)
        # surge_peak = np.amax(surge, axis=1)
        # max_volume = (subsections_div.size * params.l_seg * surge_peak**2) / (2 * Topo.slope[div])
        # volume_div[volume_div[:,div] > max_volume, div] = max_volume[volume_div[:,div] > max_volume]
            
        # Calc water height
        height_div[:,div] = np.sqrt((2 * volume_div[:, div] * Topo.slope[div]) / (params.l_seg * subsections_div.size))  # Water height on triangular prism coast
    return height_div, volume_div


def generate_groups(div_data):
    # Get groupings based on water travel distance

    divs = div_data["div"].to_numpy()
    groups = []
    for d in divs:
        start = d - params.travel_dist  # start of group, inclusive
        if d < params.travel_dist:
            start = 0

        end = d + params.travel_dist  # end of group, inclusive
        if d + params.travel_dist > divs.size:
            end = divs.size - 1

        group = divs[start:end+1]
        groups.append((group, group.size))  # Returns list of touples with group indices and size
    return groups


def calc_group_vol(groups, volume_div):
    # Sum volume for each group

    volume_grouped = np.zeros((volume_div.shape[0], len(groups)))
    for div in range(len(groups)):
        volume_grouped[:, div] = np.sum(volume_div[:, groups[div][0]], axis=1)
    return volume_grouped


def calc_group_h(Topo, groups, volume_grouped, surge_peak):
    # Average height over group for center division
    height_group = np.zeros(volume_grouped.shape)
    
    for div in range(height_group.shape[1]):
        avg_slope = np.mean(Topo.slope[groups[div][0]])
        subsections = [i for i, d in enumerate(Topo.all_divs) if d in groups[div][0]]
        group_length = len(subsections) * params.l_seg
        height_group[:, div] = np.minimum(np.sqrt((2 * volume_grouped[:, div] * avg_slope) / group_length), surge_peak)  # Limit water height to surge peak 
    return height_group
