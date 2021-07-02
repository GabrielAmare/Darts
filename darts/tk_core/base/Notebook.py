from tkinter import *

from tools import EventBeacon


def caller(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


class NoteBook(Frame, EventBeacon):
    def __init__(self, root, align=X, **cfg):
        Frame.__init__(self, root, **cfg)
        EventBeacon.__init__(self)

        if align not in [LEFT, CENTER, X, RIGHT]:
            raise ValueError(align)

        self.align = align

        self.tabs = {}
        self.active_tab = None

        self.styles = {
            "active": dict(),
            "enabled": dict(),
            "disabled": dict()
        }

        self.head = Frame(self)
        self.body = Frame(self)

        self.head.pack(side=TOP, fill=X if self.align in [LEFT, X, RIGHT] else NONE)
        self.body.pack(side=TOP, fill=BOTH, expand=True)

    def _show(self, key: str):
        if key in self.tabs:
            data = self.tabs[self.active_tab]
            widget = data["widget"]
            button = data["button"]

            widget.pack(side=TOP, fill=BOTH, expand=True)
            if data["disabled"]:
                button.configure(state="disabled", **self.styles["disabled"])
            else:
                button.configure(state="disabled", **self.styles["active"])

    def _hide(self, key: str):
        if key in self.tabs:
            data = self.tabs[self.active_tab]
            widget = data["widget"]
            button = data["button"]

            if data["disabled"]:
                button.configure(state="disabled", **self.styles["disabled"])
            else:
                button.configure(state="normal", **self.styles["enabled"])
            widget.pack_forget()

    def append(self, key: str, text: str, cls: type, cfg: dict, disabled: bool = False):
        """Add a new tab to the notebook"""
        button = Button(
            self.head,
            text=text,
            command=caller(self.active, key),
            **self.styles["disabled" if disabled else "enabled"]
        )
        widget = cls(self.body, **cfg)
        self.tabs[key] = {
            "button": button,
            "widget": widget,
            "disabled": disabled
        }
        button.pack(
            side=RIGHT if self.align == RIGHT else LEFT,
            fill=BOTH if self.align == X else Y,
            expand=self.align == X,
        )
        return button, widget

    def remove(self, key: str):
        if key in self.tabs:
            data = self.tabs.pop(key)
            data["widget"].destroy()
            data["button"].destroy()

    def get(self, key: str):
        if key in self.tabs:
            return self.tabs[key]["widget"]

    def active(self, key: str):
        """Set the active tab"""
        self._hide(self.active_tab)
        self.active_tab = key
        self._show(self.active_tab)
        self.emit("active", key)

    def disable(self, key: str):
        if key in self.tabs:
            self.tabs[key]["button"].configure(state="disabled", **self.styles["disabled"])

    def enable(self, key: str):
        if key in self.tabs:
            self.tabs[key]["button"].configure(state="normal", **self.styles["enabled"])


if __name__ == '__main__':
    FONT = "Consolas 15 bold"
    STYLE = dict(bg="black", fg="white", font=FONT)
    BUTTON_ACTIVE = dict(bd=1, relief=RAISED, bg="green", fg="black", font=FONT)
    BUTTON_ENABLED = dict(bd=1, relief=RIDGE, bg="black", fg="white", font=FONT)
    BUTTON_DISABLED = dict(bd=1, relief=SUNKEN, bg="black", fg="white", font=FONT)


    class App(Tk):
        def __init__(self):
            super().__init__()
            self.geometry("800x600")

            self.nb = NoteBook(self)
            self.nb.pack(side=TOP, fill=BOTH, expand=True)

            self.nb.config(bg="black", bd=5)
            self.nb.head.config(bg="black")
            self.nb.body.config(bg="black")

            self.nb.styles["active"] = BUTTON_ACTIVE
            self.nb.styles["enabled"] = BUTTON_ENABLED
            self.nb.styles["disabled"] = BUTTON_DISABLED

            self.nb.append(key="tab1", text="Tab 1", cls=Label, cfg=dict(text="content 1", **STYLE))
            self.nb.append(key="tab2", text="Tab 2", cls=Label, cfg=dict(text="content 2", **STYLE))
            self.nb.append(key="tab3", text="Tab 3", cls=Label, cfg=dict(text="content 3", **STYLE))

            self.nb.disable("tab3")
            self.nb.active("tab1")


    app = App()

    app.mainloop()
