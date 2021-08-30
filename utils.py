# Contains utils for various tasks needed by widgets

import numpy as np
from kivy.lang import Builder
from file_utils import (
    handle_zip, handle_file, handle_neither,
    is_magnitude, is_phase, is_neither,
    same_shape
)


'''
Hides/Shows a given widget
'''
def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.opacity, wid.disabled
        wid.opacity, wid.disabled = 0, True


'''
Returns the cell design for a title cell in the
data table
'''
def get_title_cell(title):
    cell = Builder.load_string(f'''
Label:
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Line:
            width: 1.1
            rectangle: self.x, self.y, self.width, self.height
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: root.pos
            size: root.size
    font_name: 'Lato/Lato-Bold.ttf'
    text: "{title}"
    color: 0, 0, 0, 1
        ''')
    return cell


'''
Returns the cell design for a normal row cell in the
data table
'''
def get_row_cell(text):
    cell = Builder.load_string(f'''
Label:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1.1
            rectangle: self.x, self.y, self.width, self.height
    font_name: 'Lato/Lato-Regular.ttf'
    text: "{text}"
    color: 1, 1, 1, 1
        ''')
    return cell


'''
Takes in a list of file paths, processes them, and returns
two images for the magnitude and phase.
Can handle .zip, .nii.gz, .gz, .dcm and .npz files as long
as they contain the keyword 'mag' and 'phase' in their filename.
'''
def get_mag_phase(files):
    # decode from byte string
    files = [file.decode("utf-8") for file in files]

    # from file paths get magnitude and phase data
    mag = []
    phase = []
    for file in files:
        extension = file.split('.')[-1]
        if extension == "zip":
            cur_mag, cur_phase = handle_zip(file)
            mag.extend(cur_mag)
            phase.extend(cur_phase)
        else:
            if(is_magnitude(file)):
                mag.append(handle_file(file))
            if(is_phase(file)):
                phase.append(handle_file(file))
            if(is_neither(file)):
                cur_mag, cur_phase = handle_neither(file)
                mag.extend(cur_mag)
                phase.extend(cur_phase)

    # make sure all the data is of the same shape
    mag = same_shape(mag)
    phase = same_shape(phase)

    # convert data to a numpy tensor if non empty
    mag = np.array(mag) if len(mag) else None
    phase = np.array(phase) if len(phase) else None
    
    # calculate mean of mag and phase data and return
    mag = np.mean(mag, axis=0) if mag is not None else mag
    phase = np.mean(phase, axis=0) if phase is not None else phase

    return mag, phase

            




