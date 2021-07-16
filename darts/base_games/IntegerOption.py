from typing import List

from .Option import Option


class IntegerOption(Option[int]):
    def __init__(self, default: int, values: List[int]):
        super().__init__(default)
        self.values: List[int] = values

    def confirm(self, value) -> bool:
        return type(value) is int and value in self.values
