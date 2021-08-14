from numbers import Real
from tkinter import Canvas

from tools37 import geom
from .GraphicShape import GraphicShape


class Circle(geom.Circle, GraphicShape):
    create_method = Canvas.create_oval

    def __init__(self, cnv: Canvas, x: Real, y: Real, r: Real, **config):
        geom.Circle.__init__(self, x, y, r)
        GraphicShape.__init__(self, cnv, **config)

    def coords(self):
        return map(int, (self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r))

    @property
    def c(self) -> geom.Coords:
        return geom.Coords(self.x, self.y)

    @c.setter
    def c(self, value: geom.Coords):
        self.x, self.y = value
