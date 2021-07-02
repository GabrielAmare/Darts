from tkinter import *


class Interface(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)
        self._widget = None

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, value):
        if self._widget:
            self._widget.destroy()
        self._widget = value
        self._widget.pack(side=TOP, fill=BOTH, expand=True)
