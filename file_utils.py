
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
Takes in a list of numpy arrays and checks that they're
of the same shape. If not, the smaller arrays are resized to
the largest array shape
'''
def same_shape(path):
    pass


'''
Takes in the path to a file and returns the numpy
image data for it
'''
def handle_file(path):
    pass


'''
Takes in the path to a zip file and returns two
lists: a list of magnitude numpy images and a list
of phase numpy images
'''
def handle_zip(path):
    pass

'''
Takes in the path to a file that is neither for
magnitude nor for phase data and returns the magnitude
and phase numpy images if possible.
For this function I will assume this is a .npz file that
contains mag data in the first dimension and phase data in
the second dimension because that's how the model was
trained.
'''
def handle_neither(path):
    pass