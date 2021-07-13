from tkinter import *

from darts.__meta__ import APP_NAME, VERSION, ENV
from .Main import Main
from darts.app_service import app_service


class App(Tk):
    def __init__(self, default_full_screen: bool = ENV == 'PROD'):
        super().__init__()
        self.fullscreen: bool = default_full_screen

        self.title(f'{APP_NAME} - {VERSION[0]}.{VERSION[1]}.{VERSION[2]}')
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')

        self.tk.call('wm', 'iconphoto', self._w, app_service.images.get('app-logo'))

        self.widget = Main(self)
        app_service.styles.build(self.widget, 'Main')

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.quit_fullscreen)

    def on_quit(self):
        self.destroy()

    def destroy(self):
        app_service.save()
        super().destroy()

    def toggle_fullscreen(self, _):
        self.fullscreen = not self.fullscreen

    def quit_fullscreen(self, _):
        self.fullscreen = False

    @property
    def fullscreen(self):
        return self._full_screen

    @fullscreen.setter
    def fullscreen(self, value):
        self._full_screen = value
        self.attributes("-fullscreen", value)
