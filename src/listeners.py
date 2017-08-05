import sublime
import sublime_plugin

class Listeners(sublime_plugin.EventListener):
    def on_new(self, view):
        print('new!')

    def on_activated(self, view):
        print('activated')

    def on_deactivated(self, view):
        print('deactivated')

    def on_load(self, view):
        print('load!')

    def on_modified(self, view):
        print('modified!')

    def on_close(self, view):
        print('close!')
