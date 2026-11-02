import bisect

import numpy as np
from scipy.spatial import ConvexHull


def space_occupied_score(parameters_df, bat_positions, bat_id=0):
    """Score that handles space occupied by the agent in an arena
    Partition the space into coarse grid cells (0.5 m x 0.5 m) and count
    how many the agent walked over.
    Args:
        parameters_df (dict): parameter file of the simulation
        bat_positions (list of Vectors): position of bat at every timestep

    Returns:
        int: number of unique grid cells agent was in
    """

    points_of_bat_positions = []
    for bat_position_frame in bat_positions:
        points_of_bat_positions.append(
            [bat_position_frame[bat_id][0], bat_position_frame[bat_id][1]]
        )

    hull = ConvexHull(points_of_bat_positions)
    area = hull.volume
    print("Convex hull area:", area)
    return area
