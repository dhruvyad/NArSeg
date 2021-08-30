from kivy.uix.widget import Widget
from kivy.properties import (ObjectProperty)
from kivy.clock import Clock
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.button import Button

from utils import get_title_cell, get_row_cell


class ResultsTable(Widget):
    table = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ResultsTable, self).__init__(**kwargs)
        Clock.schedule_once(self.populate)
        
    def populate(self, *_):
        print('adding widgets!')

        cols = ['LVA', 'RVA', 'LICA', 'RICA', 'LECA', 'RECA']
        rows = ['VELOCITY', 'AREA', 'SHAPE']

        self.table.cols = len(cols) + 1

        self.add2table(get_title_cell(''))

        for col in cols:
            self.add2table(get_title_cell(col))

        for row in rows:
            self.add2table(get_title_cell(row))
            for _ in range(len(cols)):
                self.add2table(get_row_cell('0.0'))

    def add2table(self, widget):
        self.table.add_widget(widget)