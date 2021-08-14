from numbers import Real
from tkinter import Canvas

from tools37 import geom
from .GraphicShape import GraphicShape


class Rectangle(geom.AbsoluteBoundingBox, GraphicShape):
    create_method = Canvas.create_rectangle

    def __init__(self, cnv: Canvas, xi: Real, yi: Real, xf: Real, yf: Real, **config):
        geom.AbsoluteBoundingBox.__init__(self, xi, yi, xf, yf)
        GraphicShape.__init__(self, cnv, **config)

    def coords(self):
        return map(int, (self.xi, self.yi, self.xf, self.yf))
