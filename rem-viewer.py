__version__ = "1.0.0"
__authors__ = ['"Miguel Teixeira" <mteixeira5@gmail.com>']

from .src.main import Main

def plugin_loaded():
    Main()
