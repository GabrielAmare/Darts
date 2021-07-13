from tkinter import *


class LabelTextFlow(Label):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)
        self.texts = {}

    def _update_text(self) -> None:
        text, config = self._get_current_text()
        self.configure(text=text, **config)
        self.update_idletasks()

    def _generate_key(self) -> int:
        if self.texts:
            return max(self.texts) + 1
        else:
            return 0

    def _get_current_text(self) -> (str, dict):
        if self.texts:
            key = max(self.texts)
            text, config = self.texts[key]
            return text, config
        else:
            return "", {}

    def append(self, text: str, **config) -> int:
        key = self._generate_key()
        self.texts[key] = (text, config)
        self._update_text()
        return key

    def remove(self, key: int) -> None:
        if key in self.texts:
            self.texts.pop(key)
        self._update_text()

    def clear(self):
        self.texts = {}
        self._update_text()
