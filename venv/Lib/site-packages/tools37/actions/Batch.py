from .Action import Action


class Batch(Action):
    """
        Batch do/undo/redo multiples actions at a time
    """

    def __init__(self, *actions: Action):
        super().__init__()
        self.actions = actions

    def do(self) -> None:
        for action in self.actions:
            action.do()

    def undo(self) -> None:
        for action in reversed(self.actions):
            action.undo()

    def redo(self) -> None:
        for action in self.actions:
            action.redo()
