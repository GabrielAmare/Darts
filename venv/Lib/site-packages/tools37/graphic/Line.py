from tkinter import Canvas
from typing import List

from tools37.geom import Coords
from .GraphicShape import GraphicShape
from itertools import chain


class Line(GraphicShape):
    create_method = Canvas.create_line

    def __init__(self, cnv: Canvas, *dots: Coords, **config):
        self.dots: List[Coords] = list(dots)
        GraphicShape.__init__(self, cnv, **config)

    def coords(self):
        if len(self.dots) < 2:
            raise ValueError

        return map(int, chain(*self.dots))

    def update(self):
        try:
            super().update()

        except ValueError:
            pass
