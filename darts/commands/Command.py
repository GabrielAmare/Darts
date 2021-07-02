class Command:
    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join(
            f"{key}={repr(val)}" for key, val in self.__dict__.items()) + ")"
