class Command:
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k!s}={v!r}' for k, v in self.__dict__.items())})"
