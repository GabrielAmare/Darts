from darts.base_gui import Label
from darts.constants import VI


class VoiceInterfaceIcon(Label):
    """
        Icon which send a visual feedback about the voice interface state
    """

    def __init__(self, root, vi):
        super().__init__(root)
        SIZE = (48, 48)

        vi.on(VI.EVENTS.LISTEN.START, lambda: self.set_image("listening", size=SIZE))
        vi.on(VI.EVENTS.LISTEN.END, lambda: self.set_image("neutral", size=SIZE))
        vi.on(VI.EVENTS.LISTEN.ERROR, lambda: self.set_image("error", size=SIZE))

        vi.on(VI.EVENTS.SPEAK.START, lambda: self.set_image("speaking", size=SIZE))
        vi.on(VI.EVENTS.SPEAK.END, lambda: self.set_image("neutral", size=SIZE))

        vi.on(VI.EVENTS.ADJUST.START, lambda: self.set_image("adjusting", size=SIZE))
        vi.on(VI.EVENTS.ADJUST.END, lambda: self.set_image("neutral", size=SIZE))

        self.set_image("neutral", size=SIZE)
