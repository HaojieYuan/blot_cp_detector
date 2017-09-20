#!/usr/bin/env python
"""
    use sliding window to extract features from each block
    feature extraction is using Zernike moments algorithem
"""

import mahotas
import sys

def blank_area(window):
    """
        decide if a window is blank by mean pixel value and max pixel variance.
    """

    # Mean value threshold is aim at eliminating areas blank.
    mean_threshold = 205
    mean_value = window.mean()

    # Lower variation threshold is aim at eliminating areas without usefulinformation.
    # Higher variation threshold is aim at eliminating areas on edge of bounding box.
    var_threshold_lowerbound = 30
    var_threshold_upperbound = 200
    min_value = window.min()
    max_value = window.max()
    var_value = max_value - min_value


    if (mean_value < mean_threshold) and (var_value > var_threshold_lowerbound) and (
        var_value < var_threshold_upperbound):
        return False
    else:
        return True



def feature_extract(img, win_size=16):
    """
        Using Zernike moments algorithem to extract features from
        each window, sliding window default size is 16 X 16
        This function will return a dictionary retrieved by
        windows starting (X, Y)
    """
    height, width = img.shape
    features = {}
    for y in range(0, height-win_size):
        for x in range(0, width-win_size):
            window = img[y:y+win_size-1, x:x+win_size-1]

            # Test if the window is blank
            if blank_area(window):
                continue
            else:
                # And here we use default radious 8.
                window_feature = mahotas.features.zernike_moments(window, 8)

                # Appending feature to dict features
                features[(x, y)] = window_feature

    return features
