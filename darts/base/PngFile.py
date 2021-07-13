from tools37.files.BaseFile import BaseFile
from tkinter import PhotoImage


class PngFile(BaseFile):
    extension = '.png'

    @classmethod
    def load(cls, fp: str) -> PhotoImage:
        return PhotoImage(file=cls._parse_fp(fp))
