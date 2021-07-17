from tkinter import *

from darts.app_data import app_data
from .SelectLang import SelectLang
from .SelectPath import SelectPath


class SettingsMenu(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)

        self.select_lang = SelectLang(self)
        app_data.styles.build(self.select_lang, 'SelectLang')

        self.select_path = SelectPath(self)
        app_data.styles.build(self.select_path, 'SelectPath')
