from .Action import Action
from .ActionList import ActionList

from darts.console import console


class   ActionHandler:
    def __init__(self):
        self.actions = []
        self.index = 0
        self.length = 0

    def __iter__(self):
        return iter(self.actions)

    def __len__(self):
        return len(self.actions)

    def do(self, *actions: Action):
        if self.index < len(self):
            self.actions = self.actions[:self.index]

        for action in actions:
            action.do()
            console.print(repr(action), "DO")
            self.actions.append(action)
            self.index += 1

    def merge_last_do(self, action: Action):
        if self.index < len(self):
            self.actions = self.actions[:self.index]

        action.do()
        console.print(repr(action), "DO")
        self.actions[-1] = ActionList(self.actions[-1], action)

    def undo(self, n: int = 1):
        for _ in range(n):
            if self.index:
                self.index -= 1
                action = self.actions[self.index]
                action.undo()
                console.print(repr(action), "UNDO")
            else:
                raise Exception("No action to undo")

    def redo(self, n: int = 1):
        for _ in range(n):
            if self.index < len(self):
                action = self.actions[self.index]
                action.redo()
                console.print(repr(action), "REDO")
                self.index += 1
            else:
                raise Exception("No action to redo")

    def undo_all(self):
        self.undo(self.index)

    def redo_all(self):
        self.redo(len(self) - self.index)
