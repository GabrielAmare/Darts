from typing import Dict, List


class Emitter:
    def __init__(self):
        self._callbacks: Dict[str, List[callable]] = {}

    def emit(self, key: str, *args, **kwargs):
        """Emit ``key`` with some args & kwargs"""
        for callback in self._callbacks.get(key, []):
            callback(*args, **kwargs)

    def on(self, key: str, callback: callable):
        """Register a ``callback`` for further emits of ``key``"""
        self._callbacks.setdefault(key, [])
        self._callbacks[key].append(callback)

    @staticmethod
    def method_decorator(key):
        """Binds a method call to emit ``key`` with the method arguments"""

        def wrapper(method):
            """Wraps around a method of an Emitter subclass"""

            def wrapped(self: Emitter, *args, **kwargs):
                self.emit(key, *args, **kwargs)
                return method(self, *args, **kwargs)

            return wrapped

        return wrapper
