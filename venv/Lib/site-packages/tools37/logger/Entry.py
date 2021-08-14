from __future__ import annotations

from datetime import datetime
from typing import List, Dict

__all__ = ["Entry"]


class Entry:
    KEYS: List[str] = ['at', 'code', 'content']

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> Entry:
        """Deserialize dict to Entry."""
        return cls(at=datetime.fromisoformat(data['at']), code=data['code'], content=data['content'])

    def to_dict(self) -> Dict[str, str]:
        """Serialize Entry to dict."""
        return dict(at=self.at.isoformat(), code=self.code, content=self.content)

    @classmethod
    def new(cls, code: str, content: str) -> Entry:
        """Create a new Entry now (auto set the `at` value)"""
        return cls(at=datetime.now(), code=code, content=content)

    def __init__(self, at: datetime, code: str, content: str) -> None:
        self.at = at
        self.code = code
        self.content = content

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.at!r}, {self.code!r}, {self.content!r})"
