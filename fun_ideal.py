import numpy as np
import pandas as pd
import ideal_params as params


def ideal_water_level(topo, div_data, surge, wall_height):
    surge_height = surge["height"].to_numpy()
    shore_height = topo["shore_height"].to_numpy()
    slope = div_data["slope"].to_numpy()
    divs = div_data["div"].to_numpy()
    subsections = topo["subsection"].to_numpy()
    roughness = div_data["roughness"].to_numpy()

    h_crit = shore_height + wall_height
    surge_peak = np.max(surge_height)

    volume_div = np.zeros(divs.size)
    height_div = np.zeros(divs.size)
    for div in divs:
        vel = np.zeros(surge_height.size)
        subsections_div = subsections[(topo["div"] == div)]
        volume_sub = np.zeros(subsections_div.size)
        for i, subsection in enumerate(subsections_div):
            h_diff = surge_height - np.tile(h_crit[subsection], surge_height.size)
            vel[h_diff > 0] = ((params.l_seg * h_diff[h_diff > 0]) / (params.l_seg + 2 * h_diff[h_diff > 0])) ** (2/3) * slope[div] ** (1/2) / roughness[div]
            vel[h_diff < 0] = 0
            if wall_height[subsection] > 0:
                cwr = 0.611 + 0.075 * h_diff / np.tile(h_crit[subsection], surge_height.size) 
                vel = vel * cwr
            volume_sub[i] = np.sum(params.l_seg * params.dt * h_diff * vel)
        volume_div[div] = np.sum(volume_sub)

        # Limit water level to surge peak
        max_volume = (subsections_div.size * params.l_seg * surge_peak**2) / (2 * slope[div])
        if volume_div[div] > max_volume:
            volume_div[div] = max_volume
        height_div[div] = np.sqrt((2 * volume_div[div] * slope[div]) / (params.l_seg * subsections_div.size))
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
    volume_grouped = np.zeros(len(groups))
    for v in range(volume_grouped.size):
        volume_grouped[v] = np.sum(volume_div[groups[v][0]])
    return volume_grouped


def calc_group_h(topo, div_data, groups, volume_grouped):

    height_group = np.zeros(len(groups))
    slope = div_data["slope"].to_numpy()
    for h in range(height_group.size):
        avg_slope = np.mean(slope[groups[h][0]])
        num_subsections = [i for i, div in enumerate(topo["div"]) if div in groups[h][0]]
        group_length = len(num_subsections) * params.l_seg
        height_group[h] = np.sqrt((2 * volume_grouped[h] * avg_slope) / group_length)  # assumes 8 segments per div for now
    return height_group