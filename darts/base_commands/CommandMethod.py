from typing import Tuple, Union


class CommandMethod:
    def __init__(self, types: Tuple[type], method: callable):
        self.type: Union[type, Tuple[type]] = types[0] if len(types) == 1 else types
        self.method: callable = method

    @classmethod
    def decorator(cls, *types: type):
        def wrapper(method: callable):
            return cls(types, method)

        return wrapper
