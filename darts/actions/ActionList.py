from .Action import Action


class ActionList(Action):
    def __init__(self, *actions: Action):
        self.actions = list(actions)

    def __iter__(self):
        return iter(self.actions)

    def __len__(self):
        return len(self.actions)

    def __repr__(self):
        return "ActionList(" + ", ".join(map(repr, self.actions)) + ")"

    def __and__(self, other):
        if isinstance(other, ActionList):
            return ActionList(*self, *other)
        elif isinstance(other, Action):
            return ActionList(*self, other)
        else:
            raise Exception(f"Unable to do {type(self).__name__} & {type(other).__name__}")

    def do(self):
        for action in self.actions:
            action.do()

    def undo(self):
        for action in reversed(self.actions):
            action.undo()

    def redo(self):
        for action in self.actions:
            action.redo()

    def append(self, action):
        self.actions.append(action)

    def extend(self, actions):
        self.actions.extend(actions)


Action.List = ActionList
