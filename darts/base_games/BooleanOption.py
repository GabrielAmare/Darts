from .Option import Option


class BooleanOption(Option[bool]):
    def __init__(self, default: bool, key_false: str = 'APP.NO', key_true: str = 'APP.YES'):
        super().__init__(default)
        self.key_false: str = key_false
        self.key_true: str = key_true

    def confirm(self, value) -> bool:
        return type(value) is bool
