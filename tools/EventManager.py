class EventManager:
    def __init__(self):
        self.events = {}

    def on(self, event, callback):
        self.events.setdefault(event, [])
        self.events[event].append(callback)
        return lambda: callback in self.events[event] and self.events[event].remove(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self.events.get(event, []):
            callback(*args, **kwargs)

    def on_from(self, emitter, event, callback):
        return self.on(str(id(emitter)) + ":" + event, callback)

    def emit_from(self, emitter, event, *args, **kwargs):
        return self.emit(str(id(emitter)) + ":" + event, *args, **kwargs)
