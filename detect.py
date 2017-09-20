#!/usr/bin/env python
"""
    Offer functions to do below jobs:
    after cleaning up text and other regions,
    use this to detect if there are copy and paste in blot image.
"""

import argparse
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from FeatureExtract import feature_extract
from FLANN import udf_FLANN
from remove_text import removeText
from math import pow, sqrt
import Merge
import sys
import os
import random

def draw_rect(img, color, x, y, w, h):
    # Transform 0~1 to 0~255
    color = [i * 255 for i in color]

    for i in range(x, x+w):
        img[y, i] = color
        img[y+h, i] = color
    for i in range(y, y+h):
        img[i, x] = color
        img[i, x+w] = color

    return img

def dul_box(x, y, w, h, boxes):
    """
        remove boxes that contained in already marked boxes
    """
    # Change boxes's data structure from set to list
    boxes = list(boxes)
    for box in boxes:
        xb, yb, wb, hb = box
        # Decide if starting point is in a box
        # If so, we judge it as a dulpicate box
        # It's same for other three points.

        if ((x < xb+2) and (x > xb-2)) and ((y < yb+2) and (y > yb-2)):
                return True

    # If starting point is not contained by any box
    # we judge it as non-dulpicate box
    return False

def adjust_pos((x1, y1, w1, h1), (x2, y2, w2, h2)):
    """
        In order to make result more readable, we simply pick the
        left one as origin part, and right one as paste part.
    """
    if x1 <= x2:
        return ((x1, y1, w1, h1), (x2, y2, w2, h2))
    else:
        return ((x2, y2, w2, h2), (x1, y1, w1, h1))

def feature_pure(features, threshold=-5e-6, win_size=16):
    """
        Fine tune features with given threshold
        return list windows which was decided as copy and
        paste area.
        Input feature is like{[x,y]:(list of coordinates, list of similarities)}
        The bigger similarity is, the more similar blocks are.
    """
    # Make sure there are no duplicate boxes.
    pairs = set()
    boxes = set()

    for coordinate in features:

        neighbors, similarities = features[coordinate]

        # Here len(neighbor) should equals len(similarities)
        # Both of them should work
        # use set to save this group of boxes
        group = set()
        for i in range(0, len(neighbors)):

            # If similarity is larger than threshold,
            # we append both coordinate to boxes.
            # And due to boxes uses set as data structure,
            # the coordinate outof loop will only be recorded once.
            if similarities[i] > threshold:

                # Get box1 in xywh form
                # Note that set can not have a list element.
                # So here we store xywh as tuple.
                x1, y1 = coordinate
                box1 = (x1, y1, win_size, win_size)

                # Get box2 in xywh form
                x2, y2 = neighbors[i]
                box2 = (x2, y2, win_size, win_size)

                # Jump over if two near object was detected
                # If distance of two boxes is smaller than 2 * win_size
                # we will just jump over
                if sqrt(pow((x1-x2), 2) + pow((y1-y2), 2)) < 2 * win_size:
                    continue


                # Append two box on boxes.
                # Note can not use update here.
                # Removing dulplicate boxes at same time.

                if not dul_box(x1, y1, win_size, win_size, boxes):
                    boxes.add(box1)
                    group.add(box1)

                if not dul_box(x2, y2, win_size, win_size, boxes):
                    boxes.add(box2)
                    group.add(box2)

        # Turn set into list in order to sort it.
        # Sort it by top left coordinate.
        group = list(group)
        group = sorted(group, key=lambda box: (box[0], box[1]))
        pairs.add(tuple(group))

    return pairs
def pair_classify(pairs):
    """
        Classify pairs due to number of element in pair.
    """
    result = []

    while len(pairs) != 0:
        length = len(pairs[0])
        particular_len_pairs = []
        for pair in pairs:
            if len(pair) == length:
                particular_len_pairs.append(pair)
        for pair in particular_len_pairs:
            pairs.remove(pair)

        if length > 1:
            result.append(particular_len_pairs)

    return result

def detect(img, threshold=-5e-6):
    """
        With given image, return boxes of copy and paste area.
        (threshold is for block similarity
        default value should work fine with most cases.)
    """
    # Using sliding window get every small block's feature value
    features = feature_extract(img)

    # Find most similar blocks by comparing their feature value
    sim_features = udf_FLANN(features)

    # Get valid blocks by thresholding similarity
    pairs = feature_pure(sim_features,threshold=threshold)

    # Classify pairs due to number of element in pair.
    pairs = pair_classify(list(pairs))

    # Cluster pairs with same slope.
    result = []
    for pair_list in pairs:
        # Due to display need, we ingnore some boxes very close to
        # each other, which will result into some single box marked
        # as pair, so here we need to jump over pairs with only one element.
        if len(pair_list[0]) <= 1:
            continue

        # Pairs with same slope are clustered after merge.
        pair_list = Merge.merge(pair_list)
        result.append(pair_list)

    return result

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
        help = "Specify the image file you want to detect.")
    ap.add_argument("-s", "--svm", required = False, default='./SVM_text_detect',
        help = "Specify the SVM you want to apply for text remove.")
    ap.add_argument("-o", "--output", nargs='?', const=1, default='./',
        help = "Specify the image extraction,pure and detect output path.")
    ap.add_argument("-d", "--display", action ="store_true",
        help = "Print final result as a pop window at same time.")

    args = vars(ap.parse_args())



    image = args['image']
    image_p = os.path.join(args['output'], 'pure' + image.split(os.sep)[-1].\
                        split('.')[0] + '.png')
    image_d = os.path.join(args['output'], 'detect' + image.split(os.sep)[-1].\
                        split('.')[0] + '.png')

    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = removeText(img, args['svm'])

    # Save remove-text-image
    cv2.imwrite(image_p, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # detect alrotirhem only works with gary scale image.
    img_GRAY = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Get bounding boxes
    pairs = detect(img_GRAY)

    # Using matplot library to display image and detected copy
    # and paste area.
    if args['display']:
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
        ax.imshow(img)

    # Draw rectangles in image.
    for pair_list in pairs:
        for pair in pair_list:

            # random.random will generate a number between 0 and 1.
            color = (random.random(), random.random(), random.random())

            for x, y, w, h in pair:
                if args['display']:
                    rect = mpatches.Rectangle(
                        (x, y), w, h, fill=False, edgecolor=color, linewidth=1)
                    ax.add_patch(rect)

                img = draw_rect(img, color, x, y, w, h)

    cv2.imwrite(image_d, img)

    # Display.
    if args['display']:
        plt.show()
