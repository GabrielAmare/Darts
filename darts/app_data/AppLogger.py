import os

from tools37.colors import BLACK, RED, GREEN, CYAN, YELLOW
from tools37.logger import Log


class AppLogger:
    """This class handles the logging."""

    ERROR = 'error'
    DEBUG = 'debug'
    WARNING = 'warning'
    SUCCESS = 'success'
    INFO = 'info'
    DO = 'do'
    UNDO = 'undo'
    REDO = 'redo'
    METHOD = 'method'
    EXECUTE = 'execute'
    SAVED = 'saved'
    LOADED = 'loaded'
    CREATED = 'created'

    def __init__(self, fp: str):
        self.logger = Log(
            fp=fp,
            auto_save=True,
            auto_print=True,
            console=Log.Console(width=256, styles={
                self.ERROR: Log.Console.Style(bg=BLACK, fg=RED),
                self.DEBUG: Log.Console.Style(bg=BLACK, fg=CYAN),
                self.WARNING: Log.Console.Style(bg=BLACK, fg=YELLOW),
                self.SUCCESS: Log.Console.Style(bg=BLACK, fg=GREEN),
                self.SAVED: Log.Console.Style(bg=BLACK, fg=GREEN, bold=True, italic=True),
                self.LOADED: Log.Console.Style(bg=BLACK, fg=GREEN, bold=True, italic=True),
                self.CREATED: Log.Console.Style(bg=BLACK, fg=GREEN, bold=True, italic=True),
                self.INFO: Log.Console.Style(bg=BLACK, fg=CYAN),
                self.DO: Log.Console.Style(bg=BLACK, fg='#4ba91f'),
                self.UNDO: Log.Console.Style(bg=BLACK, fg='#a93c1f'),
                self.REDO: Log.Console.Style(bg=BLACK, fg='#4ba91f'),
                self.METHOD: Log.Console.Style(bg=BLACK, fg='#990f44'),
                self.EXECUTE: Log.Console.Style(bg=BLACK, fg='#82B741', bold=True),
            })
        )

    def warning(self, content: object):
        return self.logger.new(self.WARNING, str(content))

    def error(self, content: object):
        return self.logger.new(self.ERROR, str(content))

    def success(self, content: object):
        return self.logger.new(self.SUCCESS, str(content))

    def info(self, content: object):
        return self.logger.new(self.INFO, str(content))

    def do(self, action: object):
        return self.logger.new(self.DO, str(action))

    def redo(self, action: object):
        return self.logger.new(self.REDO, str(action))

    def undo(self, action: object):
        return self.logger.new(self.UNDO, str(action))

    def method(self, action: object):
        return self.logger.new(self.METHOD, str(action))

    def execute(self, action: object):
        return self.logger.new(self.EXECUTE, str(action))

    def saved(self, fp: str):
        return self.logger.new(self.SAVED, os.path.abspath(fp).replace('\\', '/'))

    def loaded(self, fp: str):
        return self.logger.new(self.LOADED, os.path.abspath(fp).replace('\\', '/'))

    def created(self, fp: str):
        return self.logger.new(self.CREATED, os.path.abspath(fp).replace('\\', '/'))

    def method_info(self, method):
        def wrapped(self_, *args, **kwargs):
            self.method(f"method : {self_.__class__.__name__}.{method.__name__}(...)")
            return method(self_, *args, **kwargs)

        return wrapped

    def classmethod_info(self, method):
        def wrapped(cls_, *args, **kwargs):
            self.method(f"classmethod : {cls_.__name__}.{method.__name__}(...)")
            return method(cls_, *args, **kwargs)

        return wrapped
