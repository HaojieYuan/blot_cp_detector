"""
    remove text with given image.
"""
import extract_box
import LBP_SVM
import cv2
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

def in_area(blot_area, i, j):
    for blot in blot_area:
        x, y, w, h = blot
        if i > x and i < x+w and j > y and j < y+h:
            return True

    return False


def clean_img(img, text, blot_area):
    x, y, w, h = text
    for i in range(x, x+w):
        for j in range(y, y+h):
            if in_area(blot_area, i, j):
                continue
            else:
                # cv2 get image value with img[y, x]
                img[j, i] = [255, 255, 255]

    return img

def removeText(img, svm_file):

    crop_list = extract_box.extract(img)
    blot_list = []

    kernel = np.ones((1, 1), np.uint8)
    SVM = LBP_SVM.load_SVM(svm_file)
    for x, y, w, h in crop_list:
        # preprocessing of image, improve quilty.
        crop_img = img[y: y + h, x: x + w]
        crop_img = cv2.morphologyEx(crop_img, cv2.MORPH_OPEN, kernel)

        # get SVM prediction
        prediction = LBP_SVM.make_prediction(crop_img, SVM)

        # store all blot area in a list
        if prediction == 'blot':
            blot_list.append([x, y, w, h])


    for x, y, w, h in crop_list:
        # preprocessing of image
        crop_img = img[y: y + h, x: x + w]
        crop_img = cv2.morphologyEx(crop_img, cv2.MORPH_OPEN, kernel)

        # get SVM prediction
        prediction = LBP_SVM.make_prediction(crop_img, SVM)

        if prediction == 'text':
            text = [x, y, w, h]
            # clean_area = text_without_blot(text, blot_list)
            # try to put this inside loop rather than out of loop
            img = clean_img(img, text, blot_list)

    return img
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

    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = removeText(img, args['svm'])

    # Save remove-text-image
    # Adjust color for cv2 imwrite.
    cv2.imwrite(image_p, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))


    # Using matplot library to display images.
    if args['display']:
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
        ax.imshow(img)


    # Display.
    if args['display']:
        plt.show()
