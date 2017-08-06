import sublime
import sublime_plugin

class Label:
    view = None
    region = None

    def __init__(self, view, region):
        self.view = view
        self.region = region

    def enable(self):
        return sublime.Phantom(self.region, '<body id="my-plugin-feature"><style>div.error {background-color: red;padding: 5px;}</style><div class="error">AAAA</div></body>', sublime.LAYOUT_INLINE)

    def disable(self):
        print('disable')
