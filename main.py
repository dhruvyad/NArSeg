from kivy.app import App
from kivy.core.window import Window # to change window size

from widgets.interface import NArSegInterface
from widgets.image import MedicalImage
from widgets.table import ResultsTable


class NArSegApp(App):
    def build(self):
        Window.size = (960, 800)
        interface = NArSegInterface()
        return interface


if __name__ == "__main__":
    NArSegApp().run()