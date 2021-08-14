from tkinter import Frame, Label, Button, LEFT, BOTH, NSEW, NS, E, W
from .entries import TypedEntry


class FormHandler(Frame):
    def __init__(self, root, confirm, cancel=None, **cfg):
        super().__init__(root, **cfg)

        self.confirm_button = Button(self, **confirm)
        self.confirm_button.pack(side=LEFT, fill=BOTH, expand=True, padx=2)

        if cancel:
            self.cancel_button = Button(self, **cancel)
            self.cancel_button.pack(side=LEFT, fill=BOTH, expand=True, padx=2)


class SimpleForm(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)

        self.rows = []
        self.getters = {}
        self.handler = None
        self.on_confirm = None

    def add_entry(self, name, type_, padx=0, pady=0, **cfg):
        assert not self.handler, f"Can't add entries after handler have been set"
        row = len(self.rows)

        label = Label(self, text=cfg.pop("label", name), **cfg)
        label.grid(row=row, column=0, sticky=NS + E, padx=padx, pady=pady)

        entry = TypedEntry(self, type_, **cfg)
        entry.grid(row=row, column=1, sticky=NS + W, padx=padx, pady=pady)

        self.getters[name] = entry.get

        self.rows.append(dict(type="label+entry", widgets=[label, entry]))
        if row == 0:
            entry.focus()

        return label, entry

    def set_handler(self, confirm, cancel, **cfg):
        assert not self.handler, f"Can't redefine handler"
        row, padx, pady = len(self.rows), cfg.pop('padx', 0), cfg.pop('pady', 0)
        command = confirm.pop("command")
        if command:
            confirm["command"] = lambda: command({name: getter() for name, getter in self.getters.items()})
        self.handler = FormHandler(self, confirm, cancel, **cfg)
        self.handler.grid(row=row, column=0, columnspan=2, sticky=NSEW, padx=padx, pady=pady)
