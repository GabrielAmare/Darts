import os
import random
from typing import List, Union, Dict

from tools37 import MultiLang, JsonLoader

from darts.constants import TextMode
from darts.functions import is_str
from .AppLogger import AppLogger


def parse_text_normal(data: Union[str, List[str]]) -> str:
    """Parse the text in normal mode."""
    if isinstance(data, str):
        return data

    else:
        raise ValueError(data)


def parse_text_random(data: Union[str, List[str]]) -> str:
    """Parse the text in random mode."""
    if isinstance(data, str):
        return data

    elif isinstance(data, list) and all(map(is_str, data)):
        return random.choice(data)

    else:
        raise ValueError(data)


def parse_text_multiline(data: Union[str, List[str]]) -> str:
    """Parse the text in multiline mode."""
    if isinstance(data, str):
        return data

    elif isinstance(data, list) and all(map(is_str, data)):
        return '\n'.join(data)

    else:
        raise ValueError(data)


def parse_text(data: Union[str, List[str]], mode: TextMode) -> str:
    """Parse the text accordingly to the specified mode."""
    if mode is TextMode.NORMAL:
        return parse_text_normal(data)

    elif mode is TextMode.RANDOM:
        return parse_text_random(data)

    elif mode is TextMode.MULTILINE:
        return parse_text_multiline(data)

    else:
        raise ValueError(mode)


def apply_text_config(text: str, config: Dict[str, object]) -> str:
    """Replace text occurences of <key> by val where config is {key: val}."""
    for key, val in config.items():
        text = text.replace(f"<{key}>", str(val))

    return text


class AppMessages:
    """This class handle all the multi-lang stuff."""

    def __init__(self, lang_ISO_639_1: str, logger: AppLogger):
        self.ml: MultiLang = MultiLang(lang=lang_ISO_639_1)
        self.logger: AppLogger = logger

    @property
    def lang_ISO_639_1(self) -> str:
        return self.ml.lang

    @lang_ISO_639_1.setter
    def lang_ISO_639_1(self, value: str):
        self.ml.lang = value

    def load_directory(self, path: str, category: str):
        if os.path.exists(path):
            self.ml.load_langs(path, category=category.upper())

    def set_lang(self, lang_ISO_639_1: str) -> None:  # deprecated
        """Change the current lang."""
        self.lang_ISO_639_1 = lang_ISO_639_1

    def translate(self, __code: str, __mode: TextMode = TextMode.NORMAL, **config) -> str:
        """Translate the multi-lang code to the right text value."""
        try:
            data = self.ml.get(__code)

        except JsonLoader.CodeNotFoundError:
            self.logger.warning(f"AppMessage.translate(__code={__code!r}, ...)"
                                f" -> translation not found for lang {self.ml.lang} !")
            return __code

        text = parse_text(data, __mode)

        if config:
            text = apply_text_config(text, config)

        return text

    def auto(self, __code: str, __setter: callable, __mode: TextMode = TextMode.NORMAL, **config) -> str:
        """Automatically calls the setter when the multi-lang lang changes."""
        callback = lambda: __setter(self.translate(__code, __mode, **config))
        self.ml.subscribe(callback)
        return self.translate(__code, __mode, **config)
