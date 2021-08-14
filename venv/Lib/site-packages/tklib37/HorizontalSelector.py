from tkinter import Canvas


class HorizontalSelector(Canvas):
    def __init__(self, root, value=0.5, min_value=0, max_value=1, callback=None, pointer_config=None, pointer_width=6,
                 **cfg):
        super().__init__(root, **cfg)

        if pointer_config is None:
            pointer_config = {}

        self.pointer = self.create_rectangle(0, 0, 0, 0, **pointer_config)

        self.min_value = min_value
        self.max_value = max_value

        self.callback = callback

        self.pointer_width = pointer_width
        self.mousedown = False

        self.bind("<Button-1>", self.on_click, add=True)
        self.bind("<ButtonRelease-1>", self.on_release, add=True)
        self.bind("<Motion>", self.on_motion, add=True)
        self.bind("<Configure>", self.update, add=True)

        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        if self.callback:
            self.callback(self._value)
        self.update()

    def on_click(self, evt):
        if not self.mousedown:
            self.mousedown = True
            self.value = self._mouse_to_value(evt.x)

    def on_release(self, evt):
        if self.mousedown:
            self.mousedown = False
            self.value = self._mouse_to_value(evt.x)

    def on_motion(self, evt):
        if self.mousedown:
            self.value = self._mouse_to_value(evt.x)

    @property
    def delta(self):
        return self.max_value - self.min_value

    @property
    def rwidth(self):
        return (self.winfo_width() - self.pointer_width) or 1

    def _mouse_to_value(self, x):
        p = (x - self.pointer_width // 2) / self.rwidth
        if p < 0:
            return self.min_value
        elif p > 1:
            return self.max_value
        else:
            return self.min_value + p * self.delta

    def _value_to_mouse(self):
        return self.pointer_width // 2 + (self.value - self.min_value) * self.rwidth / self.delta

    def update(self, _=None):
        mouse_x = self._value_to_mouse()
        self.coords(
            self.pointer,
            mouse_x - self.pointer_width // 2,
            0,
            mouse_x + self.pointer_width // 2,
            self.winfo_height()
        )


if __name__ == '__main__':
    from tkinter import Tk

    win = Tk()

    HorizontalSelector(win,
                       bg="gray", width=300, height=40, bd=1, relief="ridge", highlightthickness=0,
                       callback=lambda value: print(value),
                       pointer_config=dict(fill="white")).pack(side="top")
    HorizontalSelector(win,
                       bg="gray", width=300, height=40, bd=1, min_value=1, max_value=0, relief="ridge",
                       highlightthickness=0,
                       callback=lambda value: print(value),
                       pointer_config=dict(fill="white")).pack(side="top")

    win.mainloop()
