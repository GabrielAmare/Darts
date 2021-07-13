from typing import List, Sequence

from .Action import Action
from .ActionList import ActionList


class ActionStack:
    def __init__(self):
        self.actions: List[Action] = []

    def append(self, action: Action) -> None:
        """Append action to the stack."""
        self.actions.append(action)

    def extend(self, actions: Sequence[Action]) -> None:
        """Extend actions to the stack."""
        self.actions.extend(actions)

    def clear(self) -> None:
        """Clear the actions in the stack."""
        self.actions = []

    def merge(self) -> ActionList:
        """Confirm the actions in the stack and do them all at once."""
        action = ActionList(*self.actions)
        self.clear()
        return action
