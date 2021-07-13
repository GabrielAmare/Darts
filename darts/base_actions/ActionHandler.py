from typing import List

from darts.errors import NothingToUndoError, NothingToRedoError
from .Action import Action
from .ActionSequence import ActionSequence
from .ActionStack import ActionStack


class ActionHandler(ActionSequence, Action):
    def __init__(self, *actions: Action):
        super().__init__(*actions)
        self.stash: List[Action] = []
        self.stack: ActionStack = ActionStack()

    def do(self) -> None:
        """Do a new action."""
        action = self.stack.merge()
        action.do()
        self.actions.append(action)
        self.stash = []

    def undo(self):
        """Undo the last action."""
        try:
            action = self.actions.pop(-1)
        except IndexError:
            raise NothingToUndoError()

        action.undo()
        self.stash.append(action)

    def redo(self):
        """Redo the last action."""
        try:
            action = self.stash.pop(-1)
        except IndexError:
            raise NothingToRedoError()

        action.redo()
        self.actions.append(action)

    def undo_times(self, n: int = 1) -> None:
        """Undo the n-th last actions."""
        while n > 0:
            self.undo()
            n -= 1

    def redo_times(self, n: int = 1) -> None:
        """Redo the n-th last stashed actions."""
        while n > 0:
            self.redo()
            n -= 1

    def undo_all(self) -> None:
        """Undo all the actions."""
        self.undo_times(len(self.actions))

    def redo_all(self) -> None:
        """Redo all the stashed actions."""
        self.redo_times(len(self.stash))
