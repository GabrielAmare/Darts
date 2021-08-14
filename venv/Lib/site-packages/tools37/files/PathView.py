import os
from abc import ABC, abstractmethod


class PathView(ABC):
    def __init__(self, path: str):
        """

        :param file_path: The path of the file.
        """
        self.path: str = path

    def exists(self) -> bool:
        """Return True if the path exists."""
        return os.path.exists(self.path)

    @abstractmethod
    def load(self) -> None:
        """Load the view."""

    @abstractmethod
    def save(self) -> None:
        """Save the view."""
