# import the necessary packages
from LBP import LocalBinaryPatterns
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2
import matplotlib.pyplot as plt
import pickle
import os

def load_SVM(file_name):
    """
        load pre trained support vector machine using pickle
    """
    if os.path.exists(file_name):
        loaded_model = pickle.load(open(file_name, 'rb'))
        return loaded_model
    else:
        print "Invalid SVM, file doesn't exist."
        return None

def make_prediction(img, SVM):
    """
        make prediction with pretrained SVM
        please read image file with cv2.imread()
    """
    desc = LocalBinaryPatterns(8, 4)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(gray)
    data = []
    data.append(hist)

    prediction = SVM.predict(data)[0]

    return prediction


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--training", required=True,
    	help="path to the training images")
    ap.add_argument("-e", "--testing", required=True,
    	help="path to the tesitng images")
    args = vars(ap.parse_args())

    # initialize the local binary patterns descriptor along with
    # the data and label lists
    desc = LocalBinaryPatterns(8, 4)
    data = []
    labels = []

    # Training SVM
    for imagePath in paths.list_images(args["training"]):
    	# load the image, convert it to grayscale, and describe it
    	image = cv2.imread(imagePath)
    	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    	hist = desc.describe(gray)

    	# extract the label from the image path, then update the
    	# label and data lists
    	labels.append(imagePath.split("/")[-2])

    	data.append(hist)


    # train a Linear SVM on the data
    model = LinearSVC(C=100.0, random_state=42)

    model.fit(data, labels)

    filename = 'SVM_text_blot'
    pickle.dump(model, open(filename, 'wb'))
"""
    # Validate SVM
    for imagePath in paths.list_images(args["testing"]):
    	# load the image, convert it to grayscale, describe it,
    	# and classify it
    	image = cv2.imread(imagePath)
    	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    	hist = desc.describe(gray)
    	data = []
    	data.append(hist)
    	prediction = model.predict(data)[0]

    	print prediction
    	plt.imshow(image)
    	plt.show()
    	# display the image and the prediction
    	#cv2.putText(image, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
    	#	1.0, (0, 0, 255), 3)
    	#cv2.imshow("Image", image)
    	#cv2.waitKey(0)
"""
