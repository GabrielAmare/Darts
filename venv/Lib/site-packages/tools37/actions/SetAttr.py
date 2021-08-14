from .Action import Action


class SetAttr(Action):
    def __init__(self, obj: object, key: str, val: object):
        super().__init__()
        self.obj = obj
        self.key = key
        self.had = None
        self.old = None
        self.val = val

    def do(self) -> None:
        self.had = hasattr(self.obj, self.key)
        self.old = getattr(self.obj, self.key) if self.had else None
        setattr(self.obj, self.key, self.val)

    def undo(self) -> None:
        setattr(self.obj, self.key, self.old)

    def redo(self) -> None:
        setattr(self.obj, self.key, self.val)
