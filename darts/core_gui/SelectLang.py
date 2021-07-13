from tkinter import *

from darts.base_gui import ButtonTabs, Label
from darts.app_service import app_service


class SelectLang(ButtonTabs):
    def __init__(self, root):
        super().__init__(root, 'SelectLang.button')

        self.label = Label(self, code="APP.LANG")
        app_service.styles.build(self.label, 'SelectLang.label')

        self.add_lang('fr-FR')
        self.add_lang('en-GB')
        self.add_lang('en-US')

        self.disable('en-US')

        # default lang in configuration
        self.select(app_service.lang_IETF)

    def select(self, lang_IETF: str):
        super().select(lang_IETF)
        app_service.lang_IETF = lang_IETF

    def add_lang(self, lang_IETF: str, enabled: bool = True, **config) -> Button:
        country = lang_IETF.split('-', 1)[1]

        flag_image = app_service.images.get(f"flag-{country}", scale=0.75)

        return self.add_button(
            key=lang_IETF,
            enabled=enabled,
            code=f"APP.LANGS.{country}",
            image=flag_image,
            compound=RIGHT,
            **config
        )
