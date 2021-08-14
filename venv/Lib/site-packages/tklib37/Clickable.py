from tkinter import Misc


class Clickable(Misc):
    """
        Clickable widgets will handle and respond to the left click
    """

    def __init__(self):
        self._mousedown = False
        self.bind("<Button-1>", self._on_click, add=True)
        self.bind("<ButtonRelease-1>", self._on_release, add=True)
        self.bind("<Motion>", self._on_motion, add=True)

    def _on_click(self, evt):
        if not self._mousedown:
            self.on_click(evt)
            self._mousedown = True

    def _on_release(self, evt):
        if self._mousedown:
            self.on_release(evt)
            self._mousedown = False

    def _on_motion(self, evt):
        if self._mousedown:
            self.on_motion(evt)

    def on_click(self, evt):
        raise NotImplementedError

    def on_release(self, evt):
        raise NotImplementedError

    def on_motion(self, evt):
        raise NotImplementedError
