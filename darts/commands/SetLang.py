from dataclasses import dataclass

from .base import Command


@dataclass
class SetLang(Command):
    lang_IETF: str
