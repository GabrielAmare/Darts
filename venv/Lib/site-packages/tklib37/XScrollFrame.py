from tkinter import Frame, Scrollbar, Canvas, TOP, BOTTOM, BOTH, X, NW, HORIZONTAL


class XScrollFrame(Frame):
    """
        Inspired by the post at :
            https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    """

    def __init__(self, root, xscrollside=BOTTOM, **cfg):
        bg = cfg.pop("bg", None)
        super().__init__(root, **cfg)

        self.widget = None
        self._widget_id = None

        self.xscroll = Scrollbar(self, orient=HORIZONTAL)
        self.canvas = Canvas(self, highlightthickness=0, bd=1, bg=bg)

        self.xscroll.configure(command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.xscroll.set)

        self.xscroll.pack(side=xscrollside, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.canvas.bind('<Configure>', self._configure_canvas)

    def _configure_widget(self, _event):
        self.canvas.config(scrollregion=(0, 0, self.widget.winfo_reqwidth(), self.widget.winfo_reqheight()))
        if self.widget.winfo_reqheight() != self.canvas.winfo_height():
            self.canvas.config(height=self.widget.winfo_reqheight())

    def _configure_canvas(self, _event):
        if self.widget.winfo_reqheight() != self.canvas.winfo_height():
            self.canvas.itemconfigure(self._widget_id, height=self.canvas.winfo_height())

    def set_widget(self, cls, **cfg):
        self.widget = cls(self.canvas, **cfg)
        self._widget_id = self.canvas.create_window(0, 0, anchor=NW, window=self.widget)
        self.widget.bind('<Configure>', self._configure_widget)
