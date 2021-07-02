class EventBeacon:
    """Provides functions to emit/subscribe to events on the object"""

    def __init__(self):
        self._events = {}

    def on(self, event, callback):
        self._events.setdefault(event, [])
        self._events[event].append(callback)
        return lambda: callback in self._events[event] and self._events[event].remove(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self._events.get(event, []):
            callback(*args, **kwargs)
