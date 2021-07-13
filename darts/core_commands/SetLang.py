from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class SetLang(Command):
    lang_IETF: str
