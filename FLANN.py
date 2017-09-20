#!/usr/bin/env python
"""
    This will use FLANN(Fast Liner Aproximate Neaerest Neighbors)
    to detect duplicate blocks in an image.
"""

from pyflann import *
import numpy as np
import sys

def udf_FLANN(features):
    """
        Using features extracted from FeatureExtract.py
        returns a dictionary of nearest neighbors and similarity
        retrieved by window's stating X & Y.
        neigibors and similarity will be stored as (neighbor_list, sim_list)
    """
    coordinate = []
    feature_value = []

    # Save coordinate and feature value in different list.
    # Make it easier to implement FLANN
    for item in features:
        coordinate.append(item)
    for item in coordinate:
        feature_value.append(features[item])

    # flann.nn() only accept np.array(list[list])
    # without this step, there will be an error like
    # 'list' object has no attribute 'dtype'
    feature_value = np.array(feature_value)

    # Cauculate nearest neighbor with FLANN
    # Similarity here will be generated from distances
    # All we need to do is give it a minus
    # Make it the bigger similarity is, the closer they will be.
    flann = FLANN()
    result, dists = flann.nn(
        feature_value, feature_value, 4, algorithm="kmeans", branching=32, iterations=7, checks=16)

    sim_features = {}

    for i in range(0, len(coordinate)):
        # Get -dists
        for j in range(0, len(dists[i])):
            dists[i][j] = -dists[i][j]

        # Return value of result is index of coordinates,
        # So we need another list to store coordinates value.
        result_coordinates = []

        # While cauculating nearest neighbor, the block itself will
        # always be the most similar one because there are no difference,
        # So we discard the first one.
        for k in range(1, 4):
            coordinate_value = coordinate[result[i][k]]
            result_coordinates.append(coordinate_value)

        # Append (neighbor_list, sim_list) to sim features
        # This dict is retrieved by coordinate
        sim_features[coordinate[i]] = (result_coordinates, dists[i][1:])

    return sim_features
