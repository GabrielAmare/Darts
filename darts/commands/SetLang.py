from darts.commands import Command


class SetLang(Command):
    def __init__(self, lang_IETF):
        self.lang_IETF = lang_IETF
