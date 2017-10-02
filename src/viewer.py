import re
import sublime
import sublime_plugin

from .label import Label

class Viewer:
    REGEX_PATTERN = r'([0-9]*[\.]*[0-9]+)rem(?=[;|\s])'

    view = None
    regex = None
    phantoms = {}
    phantom_set = {}

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
        phantoms = self.phantoms

        for row, labels in labels_per_row.items():
            values = [label.get_value() for label in labels]

            phantoms[row] = sublime.Phantom(self.__get_row_region(row), self.__get_html(values), sublime.LAYOUT_INLINE)

        return phantoms

    def __get_labels(self, content, offset = 0):
        labels = {}

        for region in re.finditer(self.regex, content):
            label = Label(self.view, region, offset)

            row = label.get_row()
            if row not in labels:
                labels[row] = [label]
            else:
                labels[row].append(label)

        return labels

    def __draw(self, content, offset = 0):
        labels = self.__get_labels(content, offset)
        phantoms = self.__get_phantoms(labels)

        # Update phantoms and phantomsSet 
        self.phantoms = phantoms
        self.phantom_set.update(list(phantoms.values()))

    def enable(self):
        print('enable')
        lines = sublime.Region(0, self.view.size())
        content = self.view.substr(lines)

        self.__draw(content)

    def disable(self):
        print('disable')
        for row, phantom in self.phantoms.items():
          self.view.erase_regions(str(row))

        self.phantoms = {}

    def modify(self):
        print('modify')
        
        for selection in self.view.sel():
            line = self.view.line(selection)
            content = self.view.substr(line)
            offset = line.a

            # (row, col) = self.view.rowcol(line.begin())
            # (row2, col2) = self.view.rowcol(line.end())
            # print(content)
            # print(row, row2)
            
            self.__draw(content, offset)
