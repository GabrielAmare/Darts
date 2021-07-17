import tkinter as tk

from darts.app_data import app_data


class Button(tk.Button):
    """Multilang & ImageService connected Button"""

    def __init__(self, root, **cfg) -> None:
        if 'code' in cfg:
            cfg['text'] = app_data.messages.auto(cfg.pop('code'), self.set_text)

        if 'image_name' in cfg:
            cfg['image'] = app_data.images.get(
                fp=cfg.pop('image_name'),
                size=cfg.pop('image_size', None),
                scale=cfg.pop('image_scale', None)
            )

        super().__init__(root, **cfg)

    def set_text(self, text: str) -> None:
        self.config(text=text)

    def set_image(self, name: str, size=None, scale=None):
        image = app_data.images.get(fp=name, size=size, scale=scale)
        self.configure(image=image)
        self.update_idletasks()

    def disable(self) -> None:
        self.config(state='disabled')

    def enable(self) -> None:
        self.config(state='normal')
