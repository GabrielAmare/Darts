from tkinter import *
from typing import List, Type, TypeVar

W = TypeVar('W', bound=Widget)


class WidgetWrap(Frame):
    def __init__(self, root: Widget, wrap_width: int, grid_config: dict = None, **cfg):
        super().__init__(root, **cfg)
        self._wrap_width: int = wrap_width
        self.grid_config: dict = grid_config or {}
        self._widgets: List[Widget] = []

    @property
    def wrap_width(self) -> int:
        return self._wrap_width

    @wrap_width.setter
    def wrap_width(self, value: int):
        self._wrap_width = value
        self.update()

    def new_widget(self, widget_cls: Type[W], *args, **kwargs) -> W:
        widget = widget_cls(self, *args, **kwargs)

        self._widgets.append(widget)
        self.update()

        return widget

    def del_widget(self, widget: Widget):
        self._widgets.remove(widget)
        self.update()

    def update(self):
        for index, widget in enumerate(self._widgets):
            row, column = divmod(index, self.wrap_width)
            widget.grid(row=row, column=column, sticky=NSEW, **self.grid_config)

            self.grid_rowconfigure(row, weight=1)
            self.grid_columnconfigure(column, weight=1)
