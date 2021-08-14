from abc import ABC, abstractmethod


class DictInterface(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Import the object from a dict."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Export the object as a dict."""
