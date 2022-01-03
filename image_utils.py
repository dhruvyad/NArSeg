import cv2
import numpy as np
from scipy import stats
from PIL import Image, ImageEnhance

NUMBER_TO_ARTERY = {
    '1': 'RICA',
    '2': 'RVA',
    '3': 'LVA',
    '4': 'LICA',
    '5': 'LECA',
    '6': 'RECA'
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
    contours, _  = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # should be "_, contours, _" for opencv versions <= 3.4.3 (https://github.com/facebookresearch/maskrcnn-benchmark/issues/339)
    return contours

'''
Add given contours to a given image
'''
def add_contours(image, contours, color):
    image = normalize(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB) # needed if adding to mask
    return cv2.drawContours(image, contours, -1, color, 2)

'''
Takes in cv2 RGB image and a list of contour pixels as input and
returns a list of bounding boxes for the image
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
Takes in cv2 RGB image and a list of contour pixels as input and
returns the pixel values of each contour
'''
def get_pixels(image, contours):
    pixels = {}
    imdata = np.array(image)
    for contour in contours:
        contour_mask = np.zeros(image.shape[:2])
        contour_mask = cv2.drawContours(contour_mask, contour, -1, color=255, thickness=-1)
        points = np.where(contour_mask == 255)
        current_pixels = imdata[points[0], points[1]]

        value = str(stats.mode(current_pixels, axis=None)[0][0])
        value = NUMBER_TO_ARTERY[value]

        pixels[value] = [points[0], points[1]]

    return pixels

'''
Takes in cv2 RGB image and a list of contour pixels as input and
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

'''
Takes in numpy array and enhances it to make blobs
clearer
'''
def phase_enhance(image):
	image = Image.fromarray(image)
	image = image.convert('RGB')
	brightness = ImageEnhance.Brightness(image)
	image = brightness.enhance(float('inf'))
	image = image.convert('1')
	image = normalize(np.array(image))
	return image

'''
Takes in an image and a map with pixel values of each artery
and returns their velocity in a calulations map
'''
def get_velocity(image, arteries, calculations):
    for artery, pixels in arteries.items():
        if artery not in calculations:
            calculations[artery] = {}
        print(pixels)
        velocity = str(np.sum(image[pixels[0], pixels[1]]) / len(pixels) / 100)
        velocity = velocity.split('.')
        calculations[artery]['velocity'] = velocity[0] + "." + velocity[1][:2]

    return calculations

'''
Takes in an image and a map with pixel values of each artery
and returns their area in a calulations map
'''
def get_area(image, arteries, calculations):
    for artery, pixels in arteries.items():
        if artery not in calculations:
            calculations[artery] = {}
        calculations[artery]['area'] = len(pixels[0]) * 0.5
    return calculations

'''
Takes in a horizontally facing MRI image and converts it into a vertically
facing MRI image
'''
def make_vertical(image):
    image = np.rot90(image, 1)
    return image

'''
Takes in a vertically facing MRI image and converts it into a horizontally
facing MRI image
'''
def make_horizontal(image):
    image = np.rot90(image, 1)
    image = np.rot90(image, 1)
    image = np.rot90(image, 1)
    return image