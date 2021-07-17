import playsound

from darts.errors import ListenError
from tools import VoiceInterface


class AppVoice:
    def __init__(self, lang_IETF: str):
        self.vi: VoiceInterface = VoiceInterface(time_limit=2, lang_IETF=lang_IETF)

    @property
    def lang_IETF(self) -> str:
        return self.vi.lang_IETF

    @lang_IETF.setter
    def lang_IETF(self, value: str):
        self.vi.lang_IETF = value

    def set_time_limit(self, time_limit: int):
        self.vi.time_limit = time_limit

    def speak(self, message: str) -> None:
        self.vi.speak(message)

    def listen(self, delay=None, show_all: bool = False):
        try:
            return self.vi.listen(delay=delay, show_all=show_all)

        except self.vi.AudioToTextError:
            raise ListenError()

    def play(self, sound_fp: str):
        playsound.playsound(sound_fp)
