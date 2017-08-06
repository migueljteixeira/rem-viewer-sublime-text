import sublime
import sublime_plugin

from .label import Label

class Viewer:
    REGEX = '([0-9]*[\.]*[0-9]+)rem(?=[;|\s])'

    labels = None
    view = None

    def __init__(self, view):
        self.view = view
        self.labels = self.__get_labels()

    def __get_labels(self):
        # Within this view, We look for all regions that match the given regex
        regions = self.view.find_all(self.REGEX)

        return list(map(lambda region:
          Label(self.view, region), regions)
        )

    def enable(self):
        for label in self.labels:
            label.enable()

    def disable(self):
        for label in self.labels:
            label.disable()
