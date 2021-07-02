from tkinter import *

from tools import ImageService


class ImageLabel(Label):
    def __init__(self, root, path: str, **cfg):
        super().__init__(root, **cfg)
        self.path = path

    def set(self, name: str):
        fp = f"{self.path}\\{name}.png"
        image = ImageService.get(fp, size=(48, 48))
        self.configure(image=image)
        self.update_idletasks()
