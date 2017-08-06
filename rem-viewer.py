__version__ = "1.0.0"
__authors__ = ['"Miguel Teixeira" <mteixeira5@gmail.com>']

from .src.viewer import Viewer

import sublime
import sublime_plugin

rem_viewer = None

class RemViewer:
    views = {}

    def __init__(self):
        for window in sublime.windows():
            for view in window.views():
                self.__add_view(view)

    def __add_view(self, view):
        if view.id() not in self.views:
            self.views[view.id()] = Viewer(view)

    def __delete_view(self, view):
        if view.id() in self.views:
            del self.views[view.id()]

    def __enable_view(self, view):
        if view.id() in self.views:
            self.views[view.id()].enable()

    def __disable_view(self, view):
        if view.id() in self.views:
            self.views[view.id()].disable()

    def on_open(self, view):
        self.__add_view(view)

    def on_close(self, view):
        self.__delete_view(view)

    def on_modified(self, view):
        print('')

    def on_activate(self, view):
        self.__enable_view(view)

    def on_deactivated(self, view):
        self.__disable_view(view)

class Listener(sublime_plugin.EventListener):
    def on_new(self, view):
        print('on_new')
        if rem_viewer is not None:
            rem_viewer.on_open(view)

    def on_clone(self, view):
        print('on_clone')
        if rem_viewer is not None:
            rem_viewer.on_open(view)

    def on_load(self, view):
        print('on_load')
        if rem_viewer is not None:
            rem_viewer.on_open(view)

    def on_close(self, view):
        print('on_close')
        if rem_viewer is not None:
            rem_viewer.on_close(view)

    def on_modified(self, view):
        if rem_viewer is not None:
            rem_viewer.on_modified(view)

    def on_activated(self, view):
        print('on_activated')
        if rem_viewer is not None:
            rem_viewer.on_activate(view)

    def on_deactivated(self, view):
        print('on_deactivated')
        if rem_viewer is not None:
            rem_viewer.on_deactivated(view)

# Called when the Sublime's API is ready
def plugin_loaded():
    global rem_viewer
    rem_viewer = RemViewer()
