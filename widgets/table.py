from kivy.uix.widget import Widget
from kivy.properties import (ObjectProperty)
from kivy.clock import Clock
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.button import Button

from utils import get_title_cell, get_row_cell

from kivy.clock import mainthread


class ResultsTable(Widget):
    table = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ResultsTable, self).__init__(**kwargs)
        Clock.schedule_once(self.populate)

    @mainthread
    def update(self, calculations):
        print('GOT YOUR RESULTS!')
        print(calculations)
        cols = ['LVA', 'RVA', 'LICA', 'RICA', 'LECA', 'RECA']
        # rows = ['VELOCITY', 'AREA', 'FLOW']
        rows = ['V      (cm/s)', 'A   (mm^2)', 'F (cm^3/s)']

        self.table.clear_widgets()

        self.table.cols = len(cols) + 1

        self.add2table(get_title_cell(''))

        for col in cols:
            self.add2table(get_title_cell(col))

        for row in rows:
            self.add2table(get_title_cell(row))
            for col in cols:
                if col in calculations:
                    if row == rows[0]: # velocity
                        self.add2table(get_row_cell(calculations[col]['velocity']))
                    elif row == rows[1]: # area
                        self.add2table(get_row_cell(calculations[col]['area']))
                    elif row == rows[2]: # flow
                        flow = round(float(calculations[col]['area']) * float(calculations[col]['velocity']) / 100, 2)
                        self.add2table(get_row_cell(flow))
                    else:
                        self.add2table(get_row_cell('0.0'))
                else:
                    self.add2table(get_row_cell('0.0'))

    def populate(self, *_):
        print('adding widgets!')

        cols = ['LVA', 'RVA', 'LICA', 'RICA', 'LECA', 'RECA']
        rows = ['V      (cm/s)', 'A   (mm^2)', 'F (cm^3/s)']

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