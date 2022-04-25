import numpy as np
import pandas as pd
import params_ideal as params


def calc_flood_height(Topo, surge, surge_time, wall_height):

    h_crit = Topo.shore_height + wall_height
    surge_peak = np.amax(surge, axis=1)

    volume_div = np.zeros((surge.shape[0], Topo.divs.size))
    height_div = np.zeros((surge.shape[0], Topo.divs.size))
    for div in Topo.divs:
        vel = np.zeros(surge.shape)
        subsections_div = Topo.subsections[(Topo.all_divs == div)]
        volume_sub = np.zeros((surge.shape[0], subsections_div.size))
        for i, subsection in enumerate(subsections_div):
            h_diff = surge - np.ones(surge.shape) * h_crit[subsection]
            vel[h_diff > 0] = ((params.l_seg * h_diff[h_diff > 0]) / (params.l_seg + 2 * h_diff[h_diff > 0])) ** (2/3) * Topo.slope[div] ** (1/2) / Topo.roughness[div]
            vel[h_diff < 0] = 0
            if wall_height[subsection] > 0:
                cwr = 0.611 + 0.075 * h_diff / np.tile(h_crit[subsection], surge.shape) 
                vel = vel * cwr
            volume_sub[:, i] = np.sum(params.l_seg * params.dt * h_diff * vel, axis=1)
        volume_div[:, div] = np.sum(volume_sub, axis=1)

        # Limit water level to surge peak
        max_volume = (subsections_div.size * params.l_seg * surge_peak**2) / (2 * Topo.slope[div])
        volume_div[volume_div[:,div] > max_volume, div] = max_volume[volume_div[:,div] > max_volume]
            
        # Calc water height
        height_div[:,div] = np.sqrt((2 * volume_div[:, div] * Topo.slope[div]) / (params.l_seg * subsections_div.size))
    return height_div, volume_div


def generate_groups(div_data):
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
        groups.append((group, group.size))
    return groups


def calc_group_vol(groups, volume_div):
    volume_grouped = np.zeros((volume_div.shape[0], len(groups)))
    for v in range(len(groups)):
        volume_grouped[:, v] = np.sum(volume_div[:, groups[v][0]], axis=1)
    return volume_grouped


def calc_group_h(Topo, groups, volume_grouped):
    height_group = np.zeros(volume_grouped.shape)
    
    for h in range(height_group.shape[1]):
        avg_slope = np.mean(Topo.slope[groups[h][0]])
        num_subsections = [i for i, div in enumerate(Topo.all_divs) if div in groups[h][0]]
        group_length = len(num_subsections) * params.l_seg
        height_group[:, h] = np.sqrt((2 * volume_grouped[:, h] * avg_slope) / group_length)  # assumes 8 segments per div for now
    return height_group