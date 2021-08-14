import os
import random
import sys
from typing import Union, List

import gtts
import playsound
import speech_recognition as sr


def method_emitter(name):
    def wrapper(method):
        def wrapped(self, *args, **kwargs):
            self.emit(name + ":start")
            try:
                return method(self, *args, **kwargs)
            finally:
                self.emit(name + ":end")

        return wrapped

    return wrapper


class VoiceInterface:
    class AudioToTextError(Exception):
        pass

    class TextToAudioError(Exception):
        pass

    def on(self, event, callback):
        self.events.setdefault(event, [])
        self.events[event].append(callback)
        return lambda: callback in self.events[event] and self.events[event].remove(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self.events.get(event, []):
            callback(*args, **kwargs)

    def __init__(self, time_limit=5, temp_file="/tmp/temp.mp3", lang_IETF="fr-FR"):
        self.events = {}

        self.listener: sr = sr.Recognizer()

        self.time_limit: float = time_limit
        self.temp_file: str = temp_file

        self.lang_IETF = lang_IETF

    @property
    def lang_IETF(self):
        return self._lang_IETF

    @lang_IETF.setter
    def lang_IETF(self, value):
        self._lang_IETF = value

    @property
    def lang_ISO_639_1(self):
        return self.lang_IETF.split('-', 1)[0]

    @method_emitter("audio_to_text")
    def audio_to_text(self, parsed_audio, show_all: bool = False) -> Union[str, List[str]]:
        try:
            result = self.listener.recognize_google(
                parsed_audio,
                language=self.lang_IETF,
                show_all=show_all,
                flac_converter=os.path.curdir + "\\assets\\exes\\flac-win32.exe"  # /!\ this is NOT cross-platform /!\
            )
            if show_all:
                return [data["transcript"] for data in result['alternative']]
            else:
                return result
        except Exception as e:
            raise self.AudioToTextError

    @method_emitter("adjust_mic")
    def adjust_mic(self, seconds=1):
        with sr.Microphone() as microphone:
            self.listener.adjust_for_ambient_noise(microphone, duration=seconds)

    @method_emitter("listen")
    def listen(self, delay=None, show_all=False) -> Union[str, List[str]]:
        """
            This method listen to the user microphone and map the audio input to a corresponding text output
            :return: Text extracted from the user's record
        """
        with sr.Microphone() as microphone:
            parsed_audio = self.listener.listen(microphone, phrase_time_limit=delay if delay else self.time_limit)

        return self.audio_to_text(parsed_audio, show_all=show_all)

    @method_emitter("speak")
    def speak(self, text: str) -> bool:
        """
            This method reads the given text out loud
            :param text: The text to read
            :return: None
        """
        assert isinstance(text, str), text
        try:
            speech = gtts.gTTS(text=text, lang=self.lang_ISO_639_1, slow=False, lang_check=False)
        except:
            raise self.TextToAudioError

        try:
            speech.save(self.temp_file)
        except gtts.tts.gTTSError as e:
            print(e, file=sys.stderr)
            return False

        try:
            playsound.playsound(self.temp_file)
            return True
        except UnicodeDecodeError as e:
            print(e, file=sys.stderr)
            return False
        except playsound.PlaysoundException as e:
            print(e, file=sys.stderr)
            return False
        finally:
            if os.path.exists(self.temp_file) and os.path.isfile(self.temp_file):
                os.remove(self.temp_file)

    def speak_random(self, *texts):
        text = random.choice(texts)
        self.speak(text)
