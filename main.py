from matplotlib import image
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window # to change window size
from kivy.properties import (ObjectProperty, NumericProperty)
from kivy.graphics.texture import Texture
# from kivy.graphics import Rectangle, Color


import numpy as np
# from array import array
# import random
import cv2
import threading


import matplotlib.pyplot as plt

class MedicalImage(Widget):
    image = ObjectProperty(None)
    image_size = NumericProperty()
    image_prop = (0.5, 0.7) # proportion of window size

    def __init__(self, **kwargs):
        super(MedicalImage, self).__init__(**kwargs)
        self.image_size = int(min(self.size)) - 1
        # self.image_size = int(min(self.image_prop[0] * Window.width, self.image_prop[1] * Window.height)) - 1
        Window.bind(on_resize=self.resize)
        

    def render(self):
        mimage = self.get_image()
        mag = mimage[0]

        self.image_size = int(min(self.size)) - 1
        
        mag = cv2.resize(mag, dsize=(self.image_size, self.image_size), interpolation=cv2.INTER_CUBIC)

        texture = Texture.create(size=mag.shape)
        texture.blit_buffer(mag.tostring(), colorfmt='luminance', bufferfmt='ubyte')

        self.image.texture = texture


    def get_image(self):
        image = np.load('HC_040.npz')
        image = image.f.arr_0.astype(np.float32)
        image = np.array(image / np.max(image) * 255, dtype=np.uint8)
        return image

    def resize(self, *args): # TODO: don't resize every single pixel, add timer to reduce computation
        self.render()


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
        self.magnitude.render()
        self.phase.render()

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


class NArSegApp(App):
    def build(self):
        Window.size = (960, 800)
        interface = NArSegInterface()
        interface.render()
        return interface





if __name__ == "__main__":
    NArSegApp().run()

