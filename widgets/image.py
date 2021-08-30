from kivy.core.window import Window
from kivy.properties import (ObjectProperty, NumericProperty)
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture


from utils import hide_widget
import numpy as np
import cv2

class MedicalImage(Widget):
    image = ObjectProperty(None)
    image_size = NumericProperty()
    image_prop = (0.5, 0.7) # proportion of window size | TODO: remove this

    def __init__(self, **kwargs):
        super(MedicalImage, self).__init__(**kwargs)
        self.image_size = int(min(self.size)) - 1
        # self.image_size = int(min(self.image_prop[0] * Window.width, self.image_prop[1] * Window.height)) - 1
        Window.bind(on_resize=self.resize)

    '''
    Takes in a numpy image and renders it on the widget
    '''
    def render(self, image):
        hide_widget(self.image, False)

        image = np.array(image / np.max(image) * 255, dtype=np.uint8)

        self.image_size = int(min(self.size)) - 1
        
        image = cv2.resize(image, dsize=(self.image_size, self.image_size), interpolation=cv2.INTER_CUBIC)

        texture = Texture.create(size=image.shape)
        texture.blit_buffer(image.tostring(), colorfmt='luminance', bufferfmt='ubyte')

        self.image.texture = texture
        self.texture = texture


    def get_image(self):
        image = np.load('HC_040.npz')
        image = image.f.arr_0.astype(np.float32)
        image = np.array(image / np.max(image) * 255, dtype=np.uint8)
        return image

    def resize(self, *args): # TODO: don't resize every single pixel, add timer to reduce computation
        hide_widget(self.image, True) # TODO: remove hide image and change to hide only when files are unavailable
        # self.render() # TODO: add this back in later to make resize adjustment possible