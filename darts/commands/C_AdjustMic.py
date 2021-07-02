from darts.commands import Command


class C_AdjustMic(Command):
    def __init__(self, seconds: int = 1):
        self.seconds = seconds
