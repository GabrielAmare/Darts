from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True, order=True)
class _Binder:
    type: type
    method: callable


def bind_to(t: type):
    def wrapper(m: callable):
        return _Binder(t, m)

    return wrapper


class CommandManager:
    commands: Dict[type, callable] = {}

    def __init_subclass__(cls, **kwargs):
        cls.commands: Dict[type, callable] = {}

        for name, binder in cls.__dict__.items():
            if isinstance(binder, _Binder):
                cls.commands[binder.type] = binder.method
                setattr(cls, name, binder.method)

    def __call__(self, obj: object):
        t = type(obj)
        if t in self.commands:
            return self.commands[t](self, obj)
        elif object in self.commands:
            return self.commands[object](self, obj)
        else:
            raise TypeError(t)
