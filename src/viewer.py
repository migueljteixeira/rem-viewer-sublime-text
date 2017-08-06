import sublime
import sublime_plugin

from .label import Label

class Viewer:
    REGEX = '([0-9]*[\.]*[0-9]+)rem(?=[;|\s])'

    view = None
    regions = None
    phantoms = None
    labels = None

    def __init__(self, view):
        self.view = view
        self.regions = self.__get_regions()
        self.phantoms = self.__get_phantoms()
        self.labels = self.__get_labels()

    def __get_regions(self):
        # Within this view, we look for all regions that match the given regex
        return self.view.find_all(self.REGEX)

    def __get_phantoms(self):
        # Create a unique PhantomSet per view
        return sublime.PhantomSet(self.view, str(self.view.id()))

    def __get_labels(self):
        # Let's create a Label per region
        return list(
          map(lambda region: Label(self.view, region), self.regions)
        )

    def enable(self):
        phantoms = []

        for label in self.labels:
            phantoms.append(label.enable())

        self.phantoms.update(phantoms)

    def disable(self):
        for label in self.labels:
            label.disable()
