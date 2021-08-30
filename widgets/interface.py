from kivy.core.window import Window
from kivy.properties import (ObjectProperty)
from kivy.uix.widget import Widget
from utils import (get_mag_phase)
import threading

from kivy.clock import mainthread


from kivy.uix.behaviors import ToggleButtonBehavior


class NArSegInterface(Widget):
    magnitude = ObjectProperty(None)
    phase = ObjectProperty(None)
    filedrop_timer, filedrop_window = None, 0.01 # will wait for 10 milliseconds for file
    current_files = []

    view_buttons = None
    artery_buttons = None

    def __init__(self, **kwargs):
        super(NArSegInterface, self).__init__(**kwargs)
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

    def render(self):
        Window.bind(on_dropfile=self.filedrop)

    def on_view_button_click(self, button):
        print(button.text)

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

    @mainthread # TODO: is there a better way than to make this whole function on mainthread?
    def process_files(self):
        mag_image, phase_image = get_mag_phase(self.current_files)
        if mag_image is not None:
            self.magnitude.render(mag_image)
        if phase_image is not None:
            self.phase.render(phase_image)
        # TODO: remove below, it was added only for debugging
        filenames = [val.decode("utf-8").split('/')[-1] for val in self.current_files]
        print('processing files: ', filenames)