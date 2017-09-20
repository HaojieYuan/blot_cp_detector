# import the necessary packages
import numpy as np

#  Felzenszwalb et al.

#  These functions are added to give the compatibility with xywh boxes and xyxy boxes
def xywh2xyxy(box_xywh):
    return [box_xywh[0], box_xywh[1], box_xywh[0] + box_xywh[2], box_xywh[1] + box_xywh[3]]

def xyxy2xywh(box_xyxy):
    return [box_xyxy[0], box_xyxy[1], box_xyxy[2] - box_xyxy[0], box_xyxy[3] - box_xyxy[1]]

def non_max_suppression_slow(boxes, overlapThresh = 0.3):
	"""
		input box should be (x, y, w, h)
		will try threshold soon
	"""
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []

	_boxes = []
	for box in boxes:
		_boxes.append(xywh2xyxy(box))

	boxes = np.array(_boxes)
	# initialize the list of picked indexes
	pick = []

	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]

	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)

	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list, add the index
		# value to the list of picked indexes, then initialize
		# the suppression list (i.e. indexes that will be deleted)
		# using the last index
        # here picks the most bottom-right one
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
		suppress = [last]

		# loop over all indexes in the indexes list
		for pos in xrange(0, last):
			# grab the current index
			j = idxs[pos]

			# find the largest (x, y) coordinates for the start of
			# the bounding box and the smallest (x, y) coordinates
			# for the end of the bounding box
			xx1 = max(x1[i], x1[j])
			yy1 = max(y1[i], y1[j])
			xx2 = min(x2[i], x2[j])
			yy2 = min(y2[i], y2[j])

			# compute the width and height of the bounding box
			w = max(0, xx2 - xx1 + 1)
			h = max(0, yy2 - yy1 + 1)

			# compute the ratio of overlap between the computed
			# bounding box and the bounding box in the area list
			overlap = float(w * h) / area[j]

            # if it's a contain relationship, skip.
			if xx1 == x1[j] and xx2 == x2[j] and yy1 == y1[j] and yy2 == y2[j]:
				continue

			# if there is sufficient overlap, suppress the
			# current bounding box
			if overlap > overlapThresh:
				suppress.append(pos)


		# delete all indexes from the index list that are in the
		# suppression list
		idxs = np.delete(idxs, suppress)

	_boxes = []
	for i in pick:
         _boxes.append(boxes[i])

	boxes = []
	for box in _boxes:
		boxes.append(xyxy2xywh(box))

	# return only the bounding boxes that were picked
	return boxes

def greedy_combine_with_nms(boxes):
    """
        nms is suitable for remove boxes with large overlap.
        This is for combination job of lots region of intersts.
    """
    pass
