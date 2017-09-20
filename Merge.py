#!/usr/bin/env python
"""
    This functions helps merge small blocks to form a large bounding
    box, which is in the form of [x, y, w, h].
"""
import numpy as np
from nms import xywh2xyxy, xyxy2xywh

need_to_fill = 0.1


def get_bound(box_list):
    """
        With given box list, find the smallest bouding box
        that contains all boxes in the list.
    """
    box_xyxy_list = []
    for box in box_list:
        box_xyxy = xywh2xyxy(box)
        box_xyxy_list.append(box_xyxy)

    box_xyxy_list = np.array(box_xyxy_list)
    x1max, y1max, x2max, y2max = np.amax(box_xyxy_list, axis=0)
    x1min, y1min, x2min, y2min = np.amin(box_xyxy_list, axis=0)

    boundbox = xyxy2xywh([x1min, y1min, x2max, y2max])
    return boundbox

def distance_with_inf(v1, v2):
    """
        preprocess infinity part for euclide distance cauculate.
    """
    result = []
    for i in range(0, len(v1)):
        if v1[i] == v2[i]:
            result.append(0)
        elif (v1[i] == float("inf") or v1[i] == -float("inf")) or \
             (v2[i] == float("inf") or v2[i] == -float("inf")):
            return float("inf")
        else:
            result.append(v1[i] - v2[i])

    result = np.array(result)

    return np.linalg.norm(result)

def merge(pair_list, threshold=need_to_fill):
    """
        Merge boxes pairs with similar slope.
    """
    pair_list = list(pair_list)
    slope_list = []
    # Calculate slope of the starting coordinate of
    # every other box to the first box in the tuple.
    for pair in pair_list:
        # Get the first boxe's coordinate.
        # Due to the former process, the first box will be
        # the one on the left side.
        if len(pair) == 1:
            continue
        x0, y0, w0, h0 = pair[0]

        tmp_list = []
        for i in range(1, len(pair)):
            xi, yi, wi, hi = pair[i]
            # Take copy to exact up or below place into consideration.
            if xi == x0:
                if yi > y0:
                    slope = float("inf")
                else:
                    slope = -float("inf")
            else:
                slope = (yi - y0) * 1.0 / (xi - x0)
            # tmp list will look like
            # [slope1, slope2, ...]
            tmp_list.append(slope)

        # Slope list will look like
        # [[slope1, slope2...], [slope1, slope2...], ...]
        slope_list.append(tmp_list)

    # Then we will need to find pairs with same slope.
    # And cluster the boxes.
    # Here we take slope list as a vector and calculate their distance,
    # then use a threshold to get similar ones.
    results = []

    while len(slope_list) != 0:
        # Save tuples that should be merged.
        merge_boxes = []

        # np array will make euclide distance calculation more convienent.
        vector_r = np.array(slope_list[0])
        merge_boxes.append(pair_list[0])

        # Always keep pair list and slopelist corresponding.
        slope_list = slope_list[1:]
        pair_list = pair_list[1:]


        for vector, pair in zip(slope_list, pair_list):

            # While cauculating euclide diatance, we should take infinity
            # slope into consideration as numpy can not deal with such cases.
            vector_n = np.array(vector)

            inf_exist = False
            for slope in vector:
                if slope == float("inf") or slope == -float("inf"):
                    inf_exist = True
            for slope in vector_r:
                if slope == float("inf") or slope == -float("inf"):
                    inf_exist = True

            if inf_exist:
                # Calcuate distance with some pre procss.
                distance = distance_with_inf(vector_n, vector_r)
            else:
                # Calculate distance directly with numpy function.
                distance = np.linalg.norm(vector_n - vector_r)


            if distance <= threshold:
                merge_boxes.append(pair)
                slope_list.remove(vector)
                pair_list.remove(pair)


        # Then we process merge_boxes, merge them together and append it
        # to result.
        length = len(merge_boxes[0])
        merge_boxes = np.array(merge_boxes)
        tmp = []

        for i in range(0, length):
            tmp.append(get_bound(merge_boxes[:, i]))
        results.append(tmp)

    return results
