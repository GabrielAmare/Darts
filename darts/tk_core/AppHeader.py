from tkinter import *

from .base import LabelTextFlow, ImageLabel

from darts.constants import IMAGES_FP, STYLE
from darts.functions import translate


class AppHeader(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)

        self.icon = ImageLabel(self, path=IMAGES_FP, **STYLE.APP_HEADER.ICN_CFG)
        self.icon.pack(side=LEFT, padx=10, pady=10)

        self.label_text_flow = LabelTextFlow(self, **STYLE.APP_HEADER.LBL_CFG)
        self.label_text_flow.pack(side=LEFT, fill=BOTH, expand=True)

        self.quit_button = Button(self,
                                  text=translate("APP.QUIT"),
                                  command=root.on_quit,
                                  **STYLE.APP_HEADER.BTN_CFG)
        self.quit_button.pack(side=RIGHT)

        self.set_icon("neutral")

    def set_icon(self, name):
        self.icon.set(name)

    def append_text(self, text: str, **config) -> int:
        return self.label_text_flow.append(text, **config)

    def remove_text(self, key: int) -> None:
        self.label_text_flow.remove(key)
