from pathlib import Path
from tkinter.filedialog import *

from darts.app_service import app_service
from darts.app_data import app_data
from darts.base_gui import Label, Button


class SelectPath(Frame):
    def __init__(self, root):
        super().__init__(root)

        self.title = Label(self, code='APP.SETTINGS.GAMES_FP')
        app_data.styles.build(self.title, 'SelectPath.title')

        self.label = Label(self)
        app_data.styles.build(self.label, 'SelectPath.label')

        self.button = Button(self, code='APP.BROWSE', command=self.ask_path)
        app_data.styles.build(self.button, 'SelectPath.button')

        # default lang in configuration
        self.path: str = app_data.settings.user_files

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        value = os.path.abspath(value)
        self._path = value
        app_service.games_fp = value
        self.label.config(text=value)

    def ask_path(self):
        path = self.path

        if not os.path.exists(path):
            path = str(Path().home())

        path = askdirectory(parent=self, initialdir=path)

        if path and os.path.exists(path):
            self.path = path
