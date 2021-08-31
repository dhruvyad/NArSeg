from kivy.core.window import Window
from kivy.properties import (ObjectProperty)
from kivy.uix.widget import Widget
from utils import (get_mag_phase)
import threading
from kivy.clock import mainthread
from kivy.uix.behaviors import ToggleButtonBehavior

from model.model_utils import ModelUtils


import matplotlib.pyplot as plt
import numpy as np


class NArSegInterface(Widget):
    magnitude = ObjectProperty(None) # link to magnitude image in the UI
    phase = ObjectProperty(None) # link to phase image in the UI
    filedrop_timer, filedrop_window = None, 0.01 # will wait for 10 milliseconds for file
    current_files = [] # stores the paths to all the files being used right now

    # variables to keep a list of all the toggle buttons
    view_buttons = None
    artery_buttons = None

    # store current phase and magnitude images
    magnitude_img = None
    phase_img = None

    # store model related cached data
    binary_mask = None
    binary_manual_mask = None
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

    @mainthread
    def render(self):
        if self.magnitude_img is not None:
            self.magnitude.render(self.magnitude_img)
        if self.phase_img is not None:
            self.phase.render(self.phase_img)

    def on_view_button_click(self, button):
        text = button.text
        if text == "ORIGINAL":
            print('Orig')
        if text == "BINARY":
            image = np.array([self.magnitude_img, self.phase_img])
            mask = self.model_utils.binary_pred(image)
            plt.imshow(mask)
            plt.show()
        if text == "MULTI LABEL":
            image = np.array([self.magnitude_img, self.phase_img])
            mask = self.model_utils.multilabel_pred(image)
            plt.imshow(mask)
            plt.show()

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
        mag_image, phase_image = get_mag_phase(self.current_files)
        if mag_image is not None:
            self.magnitude_img = mag_image
        if phase_image is not None:
            self.phase_img = phase_image
        self.render()
        # TODO: remove below, it was added only for debugging
        filenames = [val.decode("utf-8").split('/')[-1] for val in self.current_files]
        print('processing files: ', filenames)