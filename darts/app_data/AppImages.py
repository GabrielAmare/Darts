from tkinter import *
from typing import Optional

from darts.base import PngFile
from darts.functions import resize_image, rescale_image, is_int, memorize
from .AppLogger import AppLogger


class AppImages:
    """This class handle all the images stuff."""

    def __init__(self, root: str, logger: AppLogger):
        self.root: str = root
        self.logger = logger

    @memorize
    def get(self, fp: str, size=None, scale=None) -> Optional[PhotoImage]:
        rfp = self.root + fp

        if not PngFile.exists(rfp):
            self.logger.warning(f'{self.__class__.__name__} failed to load : {fp!r}')
            return None

        photo = PngFile.load(rfp)
        self.logger.loaded(PngFile._parse_fp(fp))

        if scale:
            photo = rescale_image(photo, scale)

        elif size:
            if isinstance(size, int):
                width, height = size, size
            elif isinstance(size, tuple) and len(size) == 2 and all(map(is_int, size)):
                width, height = size
            else:
                raise ValueError(size)

            photo = resize_image(photo, width, height)

        return photo
