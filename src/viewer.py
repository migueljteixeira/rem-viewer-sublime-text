import sublime
import sublime_plugin

from .label import Label

class Viewer:
    REGEX = '([0-9]*[\.]*[0-9]+)rem(?=[;|\s])'

    view = None
    phantoms = None
    labels = None

    def __init__(self, view):
        self.view = view
        self.phantoms = self.__get_phantoms()
        self.labels = self.__get_labels()

    def __get_phantoms(self):
        # Create a unique PhantomSet per view
        return sublime.PhantomSet(self.view, str(self.view.id()))

    def __get_labels(self):
        # Within this view, we look for all regions that match the given regex
        # and create a Label per region
        regions = self.view.find_all(self.REGEX)

        labels = {}
        for region in regions:
            label = Label(self.view, region)
            row = label.get_row()

            if row not in labels:
                labels[row] = [label]
            else:
                labels[row].append(label)

        return labels

    def __get_html(self, values):
        return """
            <body>
            <style>
                div.error {{
                    background-color: white;
                }}
            </style>
            <div class="error">
                {values}
            </div>
            </body>
        """.format(values = values)

    def __get_row_region(self, row):
        point = self.view.text_point(row, 0)
        line = self.view.line(point)

        return sublime.Region(line.end())

    def enable(self):
        phantoms = []

        for row, labels in self.labels.items():

            values = []
            for label in labels:
                values.append(label.get_value())

            phantoms.append(
                sublime.Phantom(self.__get_row_region(row), self.__get_html(values), sublime.LAYOUT_INLINE)
            )

        self.phantoms.update(phantoms)

    def disable(self):
        print('disable')
