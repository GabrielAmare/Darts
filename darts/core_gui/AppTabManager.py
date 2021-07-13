from darts.base_gui import ButtonTabs, Button


class AppTabManager(ButtonTabs):
    def add_button(self, key: str, enabled: bool = True, **config) -> Button:
        return super().add_button(
            key=key,
            code=f"APP.TABS.{key.upper()}",
            enabled=enabled,
            **config
        )
