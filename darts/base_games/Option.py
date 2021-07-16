from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')


class Option(Generic[T], ABC):
    def __init__(self, default: T):
        self.default: T = default

    @abstractmethod
    def confirm(self, value) -> bool:
        """Return True if the option accepts this value."""
