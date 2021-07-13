from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def do(self) -> None:
        """Do the action."""

    @abstractmethod
    def undo(self) -> None:
        """Undo the action."""

    @abstractmethod
    def redo(self) -> None:
        """Redo the action."""
