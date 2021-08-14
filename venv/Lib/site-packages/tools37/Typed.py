from enum import Enum, auto


class TypedArg(Enum):
    CLASS = auto()
    SUBCLASS = auto()


class Typed:
    __cache = {}

    def __init_subclass__(cls, **kwargs):
        for name, data in Typed.__cache.items():
            cls.__create(name, data)

        Typed.__cache = {}

    @classmethod
    def __check_arg(cls, arg, arg_type):
        if arg_type is TypedArg.CLASS:
            return type(arg) is cls
        elif arg_type is TypedArg.SUBCLASS:
            return isinstance(arg, cls)
        else:
            return isinstance(arg, arg_type)

    @classmethod
    def __create(cls, name, data):
        def method(self, *args):
            for args_type, method in data:
                if all(map(cls.__check_arg, args, args_type)):
                    return method(self, *args)

            raise TypeError(args)

        setattr(cls, name, method)

    @staticmethod
    def __register(args_type, method):
        """Register a new method by name and args_type."""
        Typed.__cache.setdefault(method.__name__, [])
        Typed.__cache[method.__name__].append((args_type, method))

    @staticmethod
    def __decorator__(*args_type):
        def wrapper(method):
            Typed.__register(args_type, method)

        return wrapper


typedmethod = Typed.__decorator__
