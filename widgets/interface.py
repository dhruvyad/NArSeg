from kivy.core.window import Window
from kivy.properties import (ObjectProperty)
from kivy.uix.widget import Widget
import threading


class NArSegInterface(Widget):
    magnitude = ObjectProperty(None)
    phase = ObjectProperty(None)
    filedrop_timer, filedrop_window = None, 0.01 # will wait for 10 milliseconds for file
    current_files = []

    def __init__(self, **kwargs):
        super(NArSegInterface, self).__init__(**kwargs)
        self.filedrop_timer = threading.Timer(self.filedrop_window, self.process_files)

    def render(self):
        Window.bind(on_dropfile=self.filedrop)

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
        self.current_files = [val.decode("utf-8").split('/')[-1] for val in self.current_files]
        print('processing files: ', self.current_files)