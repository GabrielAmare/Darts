from tkinter import *
from darts.__meta__ import APP_NAME, VERSION, ENV
from tools import ImageService
from .AppInterface import AppInterface
from ..app_config import IMAGES_FP, STYLE


class FullScreenBinded(Tk):
    def __init__(self, default_full_screen: bool = False):
        super().__init__()
        self.full_screen = default_full_screen

        self.bind("<F11>", self.toggle_fullScreen)
        self.bind("<Escape>", self.quit_fullScreen)

    def toggle_fullScreen(self, _):
        self.full_screen = not self.full_screen

    def quit_fullScreen(self, _):
        self.full_screen = False

    @property
    def full_screen(self):
        return self._full_screen

    @full_screen.setter
    def full_screen(self, value):
        self._full_screen = value
        self.attributes("-fullscreen", value)


class App(FullScreenBinded):
    def __init__(self, default_full_screen: bool = ENV == "PROD"):
        super().__init__(default_full_screen)
        self.title(f"{APP_NAME} - {VERSION[0]}.{VERSION[1]}.{VERSION[2]}")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        self.tk.call('wm', 'iconphoto', self._w, ImageService.load(IMAGES_FP + "app-logo.png"))

        self.interface = AppInterface(self, **STYLE.APP_INTERFACE.CFG)
        self.interface.pack(side=TOP, fill=BOTH, expand=True)

        self.interface.on_main_menu()

    def on_quit(self):
        self.destroy()
