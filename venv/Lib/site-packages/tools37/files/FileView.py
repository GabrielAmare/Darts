from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Generic

from .PathView import PathView

E = TypeVar('E')


class FileView(Generic[E], PathView, ABC):
    def __init__(self, path: str, factory: Type[E], resource: E = None):
        super().__init__(path)
        self.factory: Type[E] = factory
        self.resource: Optional[E] = resource

    @abstractmethod
    def load(self) -> None:
        """Load the file as resource."""

    @abstractmethod
    def save(self) -> None:
        """Save the resource as file."""
