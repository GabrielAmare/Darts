from .Action import Action


class Append(Action):
    def __init__(self, obj: list, item: object):
        super().__init__()
        self.obj = obj
        self.item = item

    def do(self) -> None:
        self.obj.append(self.item)

    def undo(self) -> None:
        self.obj.pop(-1)

    def redo(self) -> None:
        self.obj.append(self.item)
