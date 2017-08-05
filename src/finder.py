import sublime
import sublime_plugin

# 1remeee

class Finder:
    colors = None

    def __init__(self, view):
        self.colors = view.find_all('([0-9]*[\.]*[0-9]+)rem')
        for color in self.colors:
            print(view.substr(color))
