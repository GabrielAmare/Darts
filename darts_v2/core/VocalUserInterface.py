from vi37 import VoiceInterface

from .Application import Application


class VocalUserInterface(VoiceInterface):
    def __init__(self, app: Application):
        self.app = app
        super().__init__(self.app.lang_IETF)
        self.app.map_to("lang_IETF", self)

    def speak(self, text: str, block: bool = False):
        self.app.feedback_icon = "speaking"
        duration = super().speak(text, block)
        return duration

    def listen(self, delay=None, show_all: bool = False, save_audio: str = ""):
        self.app.feedback_icon = "listening"
        result = super().listen(delay, show_all=show_all, save_audio=save_audio)
        self.app.feedback_icon = "neutral"
        return result

    def adjust(self, seconds=1):
        self.app.feedback_icon = "adjust"
        super().listen(seconds)
        self.app.feedback_icon = "neutral"
