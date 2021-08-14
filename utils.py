from kivy.lang import Builder


def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


def get_title_cell(title):
    cell = Builder.load_string(f'''
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
    font_name: 'Lato/Lato-Bold.ttf'
    text: "{title}"
    color: 0, 0, 0, 1
        ''')
    return cell



def get_row_cell(text):
    cell = Builder.load_string(f'''
Label:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1.1
            rectangle: self.x, self.y, self.width, self.height
    font_name: 'Lato/Lato-Regular.ttf'
    text: "{text}"
    color: 1, 1, 1, 1
        ''')
    return cell


