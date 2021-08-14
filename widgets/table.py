from kivy.uix.widget import Widget
from kivy.properties import (ObjectProperty)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


import threading
from kivy.clock import Clock

from kivy.lang import Builder


class ResultsTable(Widget):
    table = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ResultsTable, self).__init__(**kwargs)
        Clock.schedule_once(self.populate)


        
    def populate(self, *args):
        print('adding widgets!')
        for _ in range(7*6):
            self.table.add_widget(self.get_cell())


    def get_cell(self):
        cell = Builder.load_string('''
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
    font_name: 'Lato/Lato-Regular.ttf'
    text: "YOLO"
    color: 0, 0, 0, 1
        ''')
        return cell
