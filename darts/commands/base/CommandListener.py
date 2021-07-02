from typing import List

from darts.console import console
from darts.vocal_errors import ListenError, TextNotFoundError
from tools import VoiceInterface


class CommandListener:
    def __init__(self, vi: VoiceInterface):
        self.vi = vi

    def listen_command(self) -> List[str]:
        try:
            texts = self.vi.listen(show_all=True)
            console.debug("texts : \n" + "\n".join(texts))
        except VoiceInterface.AudioToTextError:
            raise ListenError()

        if not texts:
            raise TextNotFoundError()

        return texts
