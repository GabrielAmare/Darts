from tkinter import *

from darts.app_styles import app_styles
from .SelectLang import SelectLang
from .SelectPath import SelectPath


class SettingsMenu(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)

        self.select_lang = SelectLang(self)
        app_styles.build(self.select_lang, 'SelectLang')

        self.select_path = SelectPath(self)
        app_styles.build(self.select_path, 'SelectPath')
