import os

from tools37 import MultiLang

from darts.styles.default import STYLE
from tools import EventManager, VoiceInterface

ASSETS_FP = "assets/"
MESSAGES_FP = f"{ASSETS_FP}/messages/"
IMAGES_FP = f"{ASSETS_FP}/images/"
EXES_FP = f"{ASSETS_FP}/exes/"

LOG_FP = f"darts_log.txt"

MESSAGES = MultiLang(lang="fr")
EVENTS = EventManager()
VI = VoiceInterface(time_limit=2, lang_IETF="fr-FR", event_manager=EVENTS)

for category in os.listdir(MESSAGES_FP):
    path = MESSAGES_FP + category
    MESSAGES.load_langs(path, category=category.upper())

STYLE = STYLE
