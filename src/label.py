import sublime
import sublime_plugin

class Label:
    view = None
    region = None
    offset = None

    def __init__(self, view, region, offset):
        self.view = view
        self.region = region
        self.offset = offset

    def get_row(self):
        (row, col) = self.view.rowcol(self.offset + self.region.start())
        return row

    def get_value(self):
        return self.region.group()
