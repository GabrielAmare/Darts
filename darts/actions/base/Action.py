class Action:
    List: type

    def __and__(self, other):
        if isinstance(other, Action.List):
            return Action.List(self, *other)
        elif isinstance(other, Action):
            return Action.List(self, other)
        else:
            raise Exception(f"Unable to do {type(self).__name__} & {type(other).__name__}")

    def do(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def redo(self):
        raise NotImplementedError
