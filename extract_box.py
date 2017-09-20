# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import os
import cv2
import nms
import logging
import sys

def extract(img):
    """
    # Check if image file exists.
    if os.path.exists(image) == False:
        logging.error("can not open %s: no such file.", image)
        sys.exit(0)
    # CV2 read image in BGR mode, need to transform it into RGB.
    img_BGR = cv2.imread(image)
    img = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
    """
    # perform selective search
    img_lbl, regions = selectivesearch.selective_search(
        img, scale=500, sigma=0.9, min_size=1)

    # delete the region which contains whole image
    regions = sorted(regions, key=lambda x: x['size'], reverse=True)

    candidates = []

    for r in regions:
        # excluding biggest retangle which contains whole image
        if r['rect'][0] == 0 and r['rect'][1] == 0:
            continue
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding parts that are too small
        x, y, w, h = r['rect']

        if w * h < 9:
            continue

        # ecludeing parts too sharp
        if w > 100 * h or h > 100 * w:
             continue

        candidates.append(r['rect'])

    # remove rectangles opverlap each other with nms technique
    candidates = nms.non_max_suppression_slow(candidates)

    return candidates
