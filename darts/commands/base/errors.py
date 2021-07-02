class InvalidCommand(Exception):
    pass


class InvalidVocalCommand(InvalidCommand):
    pass


class InvalidTextCommand(InvalidCommand):
    pass


class InvalidCommandType(Exception):
    pass
