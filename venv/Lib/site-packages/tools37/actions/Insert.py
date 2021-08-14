from .Action import Action


class Insert(Action):
    def __init__(self, obj: list, index: int, item: object):
        super().__init__()
        self.obj = obj
        self.index = index
        self.item = item

    def do(self) -> None:
        self.obj.insert(self.index, self.item)

    def undo(self) -> None:
        self.obj.pop(self.index)

    def redo(self) -> None:
        self.obj.insert(self.index, self.item)
