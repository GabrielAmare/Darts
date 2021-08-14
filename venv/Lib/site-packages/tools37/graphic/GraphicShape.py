from abc import ABC, abstractmethod
from tkinter import Canvas
from typing import Optional, Iterator


class GraphicShape(ABC):
    """Abstract graphic shape which corresponds to a Canvas element"""
    create_method: callable

    def __init__(self, cnv: Canvas, **config):
        self.cnv: Canvas = cnv
        self.uid: Optional[int] = None
        self.config: dict = config

    def update(self):
        if self.uid is None:
            self.uid = self.__class__.create_method(self.cnv, *self.coords(), **self.config)
        else:
            self.cnv.coords(self.uid, *self.coords())
            self.cnv.itemconfig(self.uid, **self.config)

    @abstractmethod
    def coords(self) -> Iterator[int]:
        """Return the coordinates of the shape."""
