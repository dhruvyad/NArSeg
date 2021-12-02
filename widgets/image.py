from kivy.core.window import Window
from kivy.properties import (ObjectProperty, NumericProperty)
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from image_utils import (make_vertical, make_horizontal)


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

        image = make_vertical(image) # TODO: remove conversions and make everything work on verticals instead
        image = np.flipud(image) # apparently blitting flips, so this corrects for it

        if(len(image.shape) == 2): # TODO: is this grayscale to RGB conversion robust? what if RGB is passed?
            image = np.array(image / np.max(image) * 255, dtype=np.uint8)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        self.image_size = int(min(self.size)) - 1
        
        image = cv2.resize(image, dsize=(self.image_size, self.image_size), interpolation=cv2.INTER_CUBIC)

        texture = Texture.create(size=image.shape[:2], colorfmt='rgb')
        texture.blit_buffer(image.tostring(), colorfmt='rgb', bufferfmt='ubyte')

        self.image.texture = texture
        self.texture = texture

    def resize(self, *args): # TODO: don't resize every single pixel, add timer to reduce computation
        hide_widget(self.image, True) # TODO: remove hide image and change to hide only when files are unavailable
        # self.render() # TODO: add this back in later to make resize adjustment possible



