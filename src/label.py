import sublime
import sublime_plugin

class Label:
    view = None
    region = None

    def __init__(self, view, region):
        self.view = view
        self.region = region

    def get_row(self):
        (row, col) = self.view.rowcol(self.region.a)
        return row

    def get_value(self):
        return self.view.substr(self.region).split("rem")[0]
