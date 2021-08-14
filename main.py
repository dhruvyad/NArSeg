from kivy.app import App
from kivy.core.window import Window # to change window size
from kivy.core.text import FontContextManager as FCM


from widgets.interface import NArSegInterface
from widgets.image import MedicalImage
from widgets.table import ResultsTable

# FCM.create('system://myapp')
# family = FCM.add_font('Lato/Lato-.ttf')

class NArSegApp(App):
    def build(self):
        Window.size = (960, 800)
        interface = NArSegInterface()
        interface.render()
        return interface


if __name__ == "__main__":
    NArSegApp().run()

