import sublime
import sublime_plugin

from .viewer import Viewer
from .listeners import Listeners

class Main:
    views = {}

    def __init__(self):
        # Initializer listeners
        Listeners()

        for window in sublime.windows():
            for view in window.views():
                self.add_view(view)

    def add_view(self, view):
        viewer = Viewer(view)

        self.views[view.id()] = viewer
        viewer.enable()
