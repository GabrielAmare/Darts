from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from tools37.files import CsvFile
from .Console import Console
from .Entry import Entry

__all__ = ["Log"]


class Log:
    Entry = Entry
    Console = Console

    @classmethod
    def load(cls, fp: str, auto_save: bool = False, auto_print: bool = False, console: Log.Console = None) -> Log:
        """Load a .csv as log content"""
        if CsvFile.exists(fp):
            data = CsvFile.load(fp)
        else:
            if auto_save:
                CsvFile.save(fp=fp, keys=Log.Entry.KEYS, data=[])
            data = []

        return cls(
            data=list(map(Log.Entry.from_dict, data)),
            fp=fp,
            auto_save=auto_save,
            auto_print=auto_print,
            console=console
        )

    def save(self, fp: str = '') -> None:
        """Save the log content to a .csv file"""
        fp = fp or self.fp
        assert fp
        CsvFile.save(fp=fp, keys=Log.Entry.KEYS, data=list(map(Log.Entry.to_dict, self.data)))
        self.fp = fp

    def __init__(self,
                 data: List[Log.Entry] = None,
                 fp: str = '',
                 auto_save: bool = False,
                 auto_print: bool = False,
                 console: Log.Console = None):
        self.data: List[Log.Entry] = data or []
        self.fp: str = fp
        self.auto_save: bool = auto_save
        self.auto_print: bool = auto_print
        self.console: Optional[Log.Console] = console

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def new(self, code: str, content: str) -> Log.Entry:
        entry = Log.Entry.new(code=code, content=content)
        self.data.append(entry)
        if self.auto_save and self.fp:
            CsvFile.add(fp=self.fp, keys=Log.Entry.KEYS, data=entry.to_dict())
        if self.console and self.auto_print:
            self.console.print(entry)
        return entry

    def findall(self, after: datetime = None, before: datetime = None, code: str = None):
        def criteria(entry: Log.Entry):
            if after and entry.at < after:
                return False

            if before and entry.at > before:
                return False

            if code and entry.code != code:
                return False

            return True

        return filter(criteria, self)
