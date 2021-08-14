from tkinter import Frame, Scrollbar, Canvas, LEFT, RIGHT, BOTH, Y, NW, VERTICAL


class YScrollFrame(Frame):
    """
        Inspired by the post at :
            https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    """

    def __init__(self, root, yscrollside=RIGHT, **cfg):
        bg = cfg.pop("bg", None)
        super().__init__(root, **cfg)

        self.widget = None
        self._widget_id = None

        self.yscroll = Scrollbar(self, orient=VERTICAL)
        self.canvas = Canvas(self, highlightthickness=0, bd=1, bg=bg)

        self.yscroll.configure(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.yscroll.set)

        self.yscroll.pack(side=yscrollside, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas.bind('<Configure>', self._configure_canvas)

    def _configure_widget(self, _event):
        self.canvas.config(scrollregion=(0, 0, self.widget.winfo_reqwidth(), self.widget.winfo_reqheight()))
        if self.widget.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.widget.winfo_reqwidth())

    def _configure_canvas(self, _event):
        if self.widget.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self._widget_id, width=self.canvas.winfo_width())

    def set_widget(self, cls, **cfg):
        self.widget = cls(self.canvas, **cfg)
        self._widget_id = self.canvas.create_window(0, 0, anchor=NW, window=self.widget)
        self.widget.bind('<Configure>', self._configure_widget)
