from typing import List

from .Option import Option


class StringOption(Option[str]):
    def __init__(self, default: str, values: List[str], literal: bool = False):
        super().__init__(default)
        self.values: List[str] = values
        self.literal: bool = literal

    def confirm(self, value) -> bool:
        return type(value) is str and value in self.values
