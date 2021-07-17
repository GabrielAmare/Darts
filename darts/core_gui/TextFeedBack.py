from darts.app_data import app_data
from darts.base_gui import LabelTextFlow


class TextFeedBack(LabelTextFlow):
    def _add_text(self, text: str, ms: int, **cfg):
        key = self.append(text, **cfg)
        if ms > 0:
            self.after(ms, self.remove, key)

    def display(self, text: str, ms: int = 0):
        self._add_text(text, ms, **app_data.styles.get_config('TextFeedBack.NORMAL'))

    def error(self, text: str, ms: int = 0):
        self._add_text(text, ms, **app_data.styles.get_config('TextFeedBack.ERROR'))

    def warning(self, text: str, ms: int = 0):
        self._add_text(text, ms, **app_data.styles.get_config('TextFeedBack.WARNING'))

    def success(self, text: str, ms: int = 0):
        self._add_text(text, ms, **app_data.styles.get_config('TextFeedBack.SUCCESS'))
