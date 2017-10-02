import sublime

class Settings:
    REM_VIEWER_SETTINGS_FILE = "rem-viewer.sublime-settings"

    def __init__(self):
        settings = sublime.load_settings(self.REM_VIEWER_SETTINGS_FILE)

        print(settings.get('file_extensions'))
