from typing import Sequence

from .Action import Action
from .ActionSequence import ActionSequence


class ActionList(ActionSequence, Action):
    def do(self) -> None:
        for action in self.actions:
            action.do()

    def undo(self) -> None:
        for action in reversed(self.actions):
            action.undo()

    def redo(self) -> None:
        for action in self.actions:
            action.redo()

    def append(self, action: Action) -> None:
        """Append an action to the list."""
        self.actions.append(action)

    def extend(self, actions: Sequence[Action]) -> None:
        """Append a sequence actions to the list."""
        self.actions.extend(actions)
