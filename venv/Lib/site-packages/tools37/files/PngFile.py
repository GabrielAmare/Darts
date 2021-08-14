from tkinter import PhotoImage

from .BaseFile import BaseFile


class PngFile(BaseFile):
    extension = '.png'

    @classmethod
    def load(cls, fp: str) -> PhotoImage:
        return PhotoImage(file=cls.parse_fp(fp))
