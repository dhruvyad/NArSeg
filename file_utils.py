# Contains functions for handling different types of files passed
# to the GUI

import nibabel.nicom.dicomwrappers as dcm
import nibabel as nib
import numpy as np
import cv2

'''
Takes in a file path and returns true if the file
is for magnitude data, otherwise returns false
'''
def is_magnitude(path):
    filename = path.split('/')[-1]
    return 'mag' in filename

'''
Takes in a file path and returns true if the file
is for magnitude data, otherwise returns false
'''
def is_phase(path):
    filename = path.split('/')[-1]
    return 'phase' in filename

'''
Takes in a file path and returns true if the file
neither for magnitude nor for phase data
'''
def is_neither(path):
    return not (is_magnitude(path) or is_phase(path))

'''
Takes in a list of numpy arrays and resizes them to
a square the size of the largest dimension among all
given array shapes
'''
def same_shape(arrays):
    if len(arrays) == 0:
        return arrays
    
    target_size = 0
    for array in arrays:
        target_size = max(array.shape[0], array.shape[1])

    resized_arrays = []
    for array in arrays:
        resized_array = cv2.resize(array, dsize=(target_size, target_size), interpolation=cv2.INTER_CUBIC)
        resized_arrays.append(resized_array)

    return resized_arrays

'''
Takes in the path to a .dcm file and returns the numpy
image data for it
'''
def dcm_to_numpy(path):
    return dcm.wrapper_from_file(path).get_pixel_array()

'''
Takes in the path to a nii.gz or .gz file and returns
the numpy image data for it
'''
def gz_to_numpy(path):
    return nib.load(path).get_fdata()

'''
Takes in the path to a .npz file and returns
the numpy image data for it
'''
def npz_to_numpy(path):
    data = np.load(path)
    return data.f.arr_0.astype(np.float32)

'''
Takes in the path to a file and returns the numpy
image data for it
'''
def handle_file(path):
    # default black image
    DEFAULT_DATA = np.zeros((512, 512))

    extension = path.split('.')[-1]
    if extension == 'dcm':
        return dcm_to_numpy(path)
    if extension == 'gz':
        return gz_to_numpy(path)
    if extension == 'npz':
        return npz_to_numpy(path)

    # if nothing matches, return the default image
    return DEFAULT_DATA


'''
Takes in the path to a zip file and returns two
lists: a list of magnitude numpy images and a list
of phase numpy images
'''
def handle_zip(path):
    pass

'''
Takes in the path to a file that is neither for
magnitude nor for phase data and returns a list of the
magnitude and phase numpy images if possible.
For this function I will assume this is a .npz file that
contains mag data in the first dimension and phase data in
the second dimension because that's how the model was
trained.
'''
def handle_neither(path):
    data = npz_to_numpy(path)
    return [data[0]], [data[1]]