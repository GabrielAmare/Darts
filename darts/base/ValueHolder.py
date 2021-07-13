from typing import List


class ValueHolder:
    def __init__(self, values: List[int] = None, start: int = 1, step: int = 1):
        self.values: List[int] = values or []
        self.start: int = start
        self.step: int = step

    def append(self, value: int):
        if value in self.values:
            raise ValueError(value)

        self.values.append(value)

    def remove(self, value: int):
        if value not in self.values:
            raise ValueError(value)

        self.values.remove(value)

    def create(self) -> int:
        value = self.start
        while value in self.values:
            value += self.step
        return value
