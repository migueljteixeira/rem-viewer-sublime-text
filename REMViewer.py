import sublime
import sublime_plugin

# 12rem

class ColorFinder:
    colors = None

    def __init__(self, view):
        self.colors = view.find_all('([0-9]*[\.]*[0-9]+)rem')
        for color in self.colors:
            print(view.substr(color))

class VisualizerView:
    view = None
    colors = None

    def __init__(self, view):
        self.view = view
        self.colors = None

    def enable(self):
        if self.view.window().active_view().id() == self.view.id():
            print('TODO: only look at active views')

        self.colors = ColorFinder(self.view)

class Visualizer:
    views = {}

    def __init__(self):
        for window in sublime.windows():
            for view in window.views():
                self.add_view(view)

    def add_view(self, view):
        visualizerView = VisualizerView(view)

        self.views[view.id()] = visualizerView
        visualizerView.enable()

def plugin_loaded():
    Visualizer()

class ColorSelection(sublime_plugin.EventListener):
    def on_new(self, view):
        print('new!')

    def on_activated(self, view):
        print('activated')

    def on_deactivated(self, view):
        print('deactivated')

    def on_load(self, view):
        print('load!')

    def on_modified(self, view):
        print('modified!')

    def on_close(self, view):
        print('close!')
