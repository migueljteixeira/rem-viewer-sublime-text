import sublime
import sublime_plugin

from .finder import Finder

class Viewer:
    view = None
    colors = None

    def __init__(self, view):
        self.view = view
        self.colors = None

    def enable(self):
        if self.view.window().active_view().id() == self.view.id():
            print('TODO: only look at active views')

        self.colors = Finder(self.view)
