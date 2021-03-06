from typing import List

from darts.errors import NothingToUndoError, NothingToRedoError
from . import ActionList
from .Action import Action
from .ActionSequence import ActionSequence
from .ActionStack import ActionStack


class ActionHandler(ActionSequence, Action):
    def __init__(self, *actions: Action):
        """

        :param actions: The list of actions that are done (and can be undone)
        :var stash: The list of undone actions (and can be redone)
        :var stack: The list of actions that are yet to do
        """
        super().__init__(*actions)
        self.stash: List[Action] = []
        self.stack: ActionStack = ActionStack()

    def do(self) -> None:
        """Do all the stacked actions in order all as a single action."""
        action = self.stack.merge()
        action.do()
        self.actions.append(action)
        self.stash = []

    def do_merge(self) -> None:
        """
            Do all the stacked actions in order all as a single action
            and merge it with the last done action if there's one.
        """
        self.do()
        if len(self.actions) >= 2:
            B = self.actions.pop(-1)
            A = self.actions.pop(-1)
            action = ActionList(A, B)
            self.actions.append(action)
    
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
