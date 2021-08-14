from tkinter import Canvas
from typing import List

from .Circle import Circle
from .GraphicShape import GraphicShape
from .Rectangle import Rectangle
from .Line import Line


class View(Canvas):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)
        self.shapes: List[GraphicShape] = []

    def create_line(self, *coords, **config) -> Line:
        shape = Line(self, *coords, **config)
        self.shapes.append(shape)
        return shape

    def create_rectangle(self, xi, yi, xf, yf, **config) -> Rectangle:
        shape = Rectangle(self, xi, yi, xf, yf, **config)
        self.shapes.append(shape)
        return shape

    def create_circle(self, x, y, r, **config) -> Circle:
        shape = Circle(self, x, y, r, **config)
        self.shapes.append(shape)
        return shape

    def update(self):
        for shape in self.shapes:
            shape.update()
