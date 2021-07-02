from tkinter import *

from darts.app_config import APP_CFG, STYLE


class KeyVal(Frame):
    def __init__(self, root, key, val, **cfg):
        super().__init__(root, **cfg)

        self.key = Label(self, text=key, **STYLE.SETTINGS_MENU.LBL_CFG)
        self.val = Button(self, text=val, **STYLE.SETTINGS_MENU.ENT_CFG)

        self.key.pack(side=LEFT, fill=BOTH, expand=True)
        self.val.pack(side=LEFT, fill=BOTH, expand=True)


class SettingsMenu(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)

        self.lang = KeyVal(self, "lang", APP_CFG["lang"], **STYLE.SETTINGS_MENU.KEYVAL_CFG)
        self.lang.pack()
