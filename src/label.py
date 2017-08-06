import sublime
import sublime_plugin

# 1remeee

class Label:
    view = None
    region = None

    def __init__(self, view, region):
        self.view = view
        self.region = region
        print(self.view)
        print(view.substr(self.region))
