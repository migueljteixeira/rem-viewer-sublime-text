import sublime
import sublime_plugin

class Label:
    view = None
    region = None

    def __init__(self, view, region):
        self.view = view
        self.region = region
        self.key = self.__get_key()

    def __get_key(self):
      return "%u %u" % (self.region.a, self.region.b)

    def enable(self):
        print('draw')
        self.view.add_regions(self.key, [self.region], 'string', "", sublime.DRAW_SOLID_UNDERLINE)

    def disable(self):
        print('disable')
