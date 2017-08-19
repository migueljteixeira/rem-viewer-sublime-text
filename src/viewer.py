import re
import sublime
import sublime_plugin

from .label import Label

class Viewer:
    REGEX_PATTERN = r'([0-9]*[\.]*[0-9]+)rem(?=[;|\s])'

    view = None
    regex = None
    phantoms = {} # phantom per row
    phantom_set = []

    def __init__(self, view):
        self.view = view
        self.regex = re.compile(self.REGEX_PATTERN)
        self.phantom_set = sublime.PhantomSet(self.view, str(self.view.id()))

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

    def __get_phantoms(self, labels_per_row):
        for row, labels in labels_per_row.items():
            values = []
            for label in labels:
                values.append(label.get_value())

            phanthom = sublime.Phantom(self.__get_row_region(row), self.__get_html(values), sublime.LAYOUT_INLINE)

            self.phantoms[row] = phanthom

        return list(self.phantoms.values())

    def __get_labels(self, content, offset = 0):
        labels = {}
        found = False

        for region in re.finditer(self.regex, content):
            label = Label(self.view, region, offset)

            row = label.get_row()
            if row not in labels:
                labels[row] = [label]
            else:
                labels[row].append(label)

            found = True

        if not found:
            print('NOTHING!')
            (row, col) = self.view.rowcol(offset)
            labels[row] = []

        return labels

    def __draw(self, content, offset = 0):
        labels = self.__get_labels(content, offset)
        phantoms = self.__get_phantoms(labels)

        self.phantom_set.update(phantoms)

    def enable(self):
        print('enable')
        lines = sublime.Region(0, self.view.size())
        content = self.view.substr(lines)

        self.__draw(content)

    def disable(self):
        print('disable')

    def modify(self):
        print('modify')
        
        for selection in self.view.sel():
            line = self.view.line(selection)
            content = self.view.substr(line)
            offset = line.a

            self.__draw(content, offset)
