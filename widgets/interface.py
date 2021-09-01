from kivy.core.window import Window
from kivy.properties import (ObjectProperty)
from kivy.uix.widget import Widget
from utils import (get_mag_phase, get_loading_screen)
from image_utils import (get_boxes, add_boxes, detect_contours, add_contours)
import threading
from kivy.clock import mainthread
from kivy.uix.behaviors import ToggleButtonBehavior
from model.model_utils import ModelUtils
import numpy as np


import matplotlib.pyplot as plt

# DEFINE MAIN CONSTANTS BELOW

# constants that are the same as button text in UI
# used to handle click events
ORIGINAL_VIEW = "ORIGINAL"
BINARY_VIEW = "BINARY"
MULTILABEL_VIEW = "MULTI LABEL"
ARTERIES_6 = "6 ARTERIES"
ARTERIES_4 = "4 ARTERIES"
# UI constants
BINARY_CONTOUR_COLOR = (255, 0, 0)



class NArSegInterface(Widget):
    magnitude = ObjectProperty(None) # link to magnitude image in the UI
    phase = ObjectProperty(None) # link to phase image in the UI
    filedrop_timer, filedrop_window = None, 0.01 # will wait for 10 milliseconds for file
    current_files = [] # stores the paths to all the files being used right now

    # variables to keep a list of all the toggle buttons
    view_buttons = None
    current_view = ORIGINAL_VIEW
    artery_buttons = None
    current_arteries = ARTERIES_6

    # store current phase and magnitude images
    magnitude_img = None
    phase_img = None

    # store model related cached data
    binary_mask = None
    binary_manual_mask = None # multilabels set manually by user
    multilabel_mask = None



    def __init__(self, **kwargs):
        super(NArSegInterface, self).__init__(**kwargs)
        # make sure file drops are sent to the filedrop() function
        Window.bind(on_dropfile=self.filedrop)
        # makes processing multiple files possible
        self.filedrop_timer = threading.Timer(self.filedrop_window, self.process_files)
        # makes sure at least one toggle button is selected at all times
        ToggleButtonBehavior.allow_no_selection = False
        # initialize other variables
        self.view_buttons = ToggleButtonBehavior.get_widgets('view_type')
        for button in self.view_buttons:
            button.bind(on_press=self.on_view_button_click)
        self.artery_buttons = ToggleButtonBehavior.get_widgets('artery_select_type')
        for button in self.artery_buttons:
            button.bind(on_press=self.on_artery_button_click)
        # get an instance of model utilities
        self.model_utils = ModelUtils()
        # initialize loading screen
        self.loading_screen = get_loading_screen()

    # reset relevant variables when new files are dropped
    def reset_variables(self):
        self.magnitude_img = None
        self.phase_img = None
        self.binary_mask = None
        self.binary_manual_mask = None
        self.multilabel_mask = None

    @mainthread
    def render(self):
        magnitude = self.magnitude_img
        phase = self.phase_img

        if self.current_view == BINARY_VIEW:
            contours = detect_contours(self.binary_mask)
            magnitude = add_contours(magnitude, contours, BINARY_CONTOUR_COLOR)
            phase = add_contours(phase, contours, BINARY_CONTOUR_COLOR)

        if self.current_view == MULTILABEL_VIEW:
            contours = detect_contours(self.multilabel_mask)
            boxes = get_boxes(self.multilabel_mask, contours)
            magnitude = add_boxes(magnitude, boxes)
            phase = add_boxes(phase, boxes)

        if magnitude is not None:
            self.magnitude.render(magnitude)
        if phase is not None:
            self.phase.render(phase)

    @mainthread
    def start_loading(self, *_):
        self.loading_screen.open(animation=False)

    @mainthread
    def end_loading(self, *_):
        self.loading_screen.dismiss()

    def get_binary_mask(self):
        image = np.array([self.magnitude_img, self.phase_img])
        self.binary_mask = self.model_utils.binary_pred(image)
        self.render()
        self.end_loading()

    def get_multilabel_mask(self):
        image = np.array([self.magnitude_img, self.phase_img])
        self.multilabel_mask = self.model_utils.multilabel_pred(image)
        self.render()
        self.end_loading()
    
    def on_view_button_click(self, button):
        view = button.text
        self.current_view = view # update current view
        if view == ORIGINAL_VIEW:
            self.render()
        if view == BINARY_VIEW:
            if self.binary_mask is not None:
                self.render()
            else:
                self.start_loading()
                threading.Thread(target=self.get_binary_mask).start()
        if view == MULTILABEL_VIEW:
            if self.multilabel_mask is not None:
                self.render()
            else:
                self.start_loading()
                threading.Thread(target=self.get_multilabel_mask).start()

    def on_artery_button_click(self, button):
        print(button.text)

    def filedrop(self, _, file_path):
        if not self.filedrop_timer.is_alive():
            self.current_files.clear()
            self.filedrop_timer = threading.Timer(self.filedrop_window, self.process_files)
            self.filedrop_timer.start()
        else:
            self.filedrop_timer.cancel()
            self.filedrop_timer = threading.Timer(self.filedrop_window, self.process_files)
            self.filedrop_timer.start()
        self.current_files.append(file_path)

    def process_files(self):
        self.reset_variables() # reset current data
        mag_image, phase_image = get_mag_phase(self.current_files)
        if mag_image is not None:
            self.magnitude_img = mag_image
        if phase_image is not None:
            self.phase_img = phase_image
        self.render()
        # TODO: remove below, it was added only for debugging
        filenames = [val.decode("utf-8").split('/')[-1] for val in self.current_files]
        print('processing files: ', filenames)