import re
import sublime
import sublime_plugin

from .label import Label

class Viewer:
    REGEX = '([0-9]*[\.]*[0-9]+)rem(?=[;|\s])'

    view = None
    phantom_set = []

    def __init__(self, view):
        self.view = view
        self.phantom_set = self.__get_phantom_set()
        self.draw()

    def __get_phantom_set(self):
        # Create a unique PhantomSet per view
        return sublime.PhantomSet(self.view, str(self.view.id()))

    def __get_labels(self, regions):
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

    def draw(self):
        # Within this view, we look for all regions that match the given regex
        regions = self.view.find_all(self.REGEX)
        labels = self.__get_labels(regions)
        phantoms = self.get_phantoms(labels)

        self.phantom_set.update(phantoms)

    def get_phantoms(self, labels_per_row):
        phantoms = []

        for row, labels in labels_per_row.items():
            values = []
            for label in labels:
                values.append(label.get_value())

            phantoms.append(
                sublime.Phantom(self.__get_row_region(row), self.__get_html(values), sublime.LAYOUT_INLINE)
            )

        return phantoms

    def enable(self):
        print('enable')

    def disable(self):
        print('disable')

    def modify(self):
        print('modify')
        line = self.view.line(self.view.sel()[0])
        content = self.view.substr(line)

        print(content)
        # print(re.findall(r"([0-9]*[\.]*[0-9]+)rem(?=[;|\s])", content))

        all_content = self.view.substr(sublime.Region(0, self.view.size()))

        regex = re.compile(r"([0-9]*[\.]*[0-9]+)rem(?=[;|\s])")
        for match in re.finditer(regex, all_content):
            (row, col) = self.view.rowcol(match.start())
            print(row)
            # print(all_content[match.start() : match.end()])
