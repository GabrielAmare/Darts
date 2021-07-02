from tkinter import *
import os


class ImageService:
    """
        Use it only after the App started
    """
    loaded = {}

    @classmethod
    def load(cls, fp: str, size=None):
        if os.path.exists(fp) and os.path.isfile(fp) and fp.endswith('.png'):
            photo = PhotoImage(file=fp)
            if size:
                photo = photo.subsample(photo.width() // size[0], photo.height() // size[1])
            cls.set(fp, photo)
            return photo

    @classmethod
    def set(cls, fp: str, photo: PhotoImage):
        cls.loaded[fp] = photo

    @classmethod
    def get(cls, fp: str, size=None):
        fp = os.path.abspath(fp)

        if fp in cls.loaded:
            photo = cls.loaded[fp]
        else:
            photo = cls.load(fp, size)

        return photo
