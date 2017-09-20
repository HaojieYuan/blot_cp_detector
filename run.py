#!/usr/bin/env python
"""
With given input pdf file,
print copy and paste areas in the images of blot.
"""

__author__ = "HaojieYuan"
__email__ = "haojie.d.yuan@gmail.com"
__version__ = "0.1"

import extract_pdf
import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
from remove_text import removeText
import random
import shutil
from detect import *

def cpfiles(source, destination):
    if not os.path.isdir(destination):
        os.makedirs(destination)
    file_name_list = os.listdir(source)
    for filename in file_name_list:
        full_name = os.path.join(source, filename)
        shutil.copy(full_name, destination)



if __name__ == '__main__':
    try:
        shutil.rmtree('./tmp')
    except OSError:
        pass
    # Clean up old tmp files.
    try :
        os.makedirs('./tmp/')
    except OSError:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required = True,
        help = "Specify the pdf file you want to extract from.")
    ap.add_argument("-s", "--svm", required = False, default='./SVM_text_detect',
        help = "Specify the SVM you want to apply for text remove.")
    ap.add_argument("-o", "--output", nargs='?', const=1, default='./',
        help = "Specify the image extraction,pure and detect output path.")
    ap.add_argument("-d", "--display", action ="store_true",
        help = "Print final result as a pop window at same time.")

    args = vars(ap.parse_args())

    image_list = extract_pdf.extract(args['file'], './tmp/')
    cpfiles('./tmp/', args['output'])

    for image in image_list:

        image_e = os.path.join(args['output'], image)
        image_p = os.path.join(args['output'], 'pure' + image.split(os.sep)[-1].\
                            split('.')[0] + '.png')
        image_d = os.path.join(args['output'], 'detect' + image.split(os.sep)[-1].\
                            split('.')[0] + '.png')

        img = cv2.imread(image_e)
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

        # Clean up.
        try:
            shutil.rmtree('./tmp')
        except OSError:
            pass
