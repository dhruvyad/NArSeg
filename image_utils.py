import cv2
import numpy as np
from scipy import stats

NUMBER_TO_ARTERY = {
    '1': 'LICA',
    '2': 'LVA',
    '3': 'RVA',
    '4': 'RICA',
    '5': 'RECA',
    '6': 'LECA'
}

'''
Normalizes a numpy array for use with OpenCV
'''
def normalize(image):
	return np.array(image / np.max(image) * 255, dtype=np.uint8)

'''
Detect the contours of a given numpy mask
'''
def detect_contours(image):
    image = normalize(image)
    _, image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
    _, contours, _  = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours

'''
Add given contours to a given image
'''
def add_contours(image, contours, color):
    image = normalize(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB) # needed if adding to mask
    return cv2.drawContours(image, contours, -1, color, 2)


'''
Taken in cv2 RGB image and a list of contour pixels as input and
adds bounding boxes to the image
'''
def get_boxes(image, contours):
    boxes = {}
    imdata = np.array(image)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        contour_mask = np.zeros(image.shape[:2])
        contour_mask = cv2.drawContours(contour_mask, contour, -1, color=255, thickness=-1)
        points = np.where(contour_mask == 255)
        pixels = imdata[points[0], points[1]]

        value = str(stats.mode(pixels, axis=None)[0][0])
        value = NUMBER_TO_ARTERY[value]

        boxes[value] = (x, y, w, h)

    return boxes

'''
Taken in cv2 RGB image and a list of contour pixels as input and
adds bounding boxes to the image
'''
def add_boxes(image, boxes):
    color = (255, 0, 0)
    text_color = (255, 255, 255)
    # text_size = 0.35
    text_size = 0.4

    image = normalize(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB) # usually interface images are all grayscale
    for label, box in boxes.items():
        (x, y, w, h) = box
        image = cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)

        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, text_size, 1)

        # image = cv2.rectangle(image, (x, y - 20), (x + tw, y), color, -1)
        image = cv2.rectangle(image, (x - 1, y - int(1.9*th)), (x + tw, y), color, -1)
        image = cv2.putText(image, label, (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, text_size, text_color, 1)

    return image