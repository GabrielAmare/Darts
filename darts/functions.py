import random

from .constants import VI, MESSAGES, LOG_FP


def log(obj):
    with open(LOG_FP, mode='a', encoding='utf-8') as file:
        file.write(f"\n{obj}")


def translate(code, rand=False, config=None):
    data = MESSAGES.get(code)
    if isinstance(data, list):
        assert rand
        text = random.choice(data)
    elif isinstance(data, str):
        text = data
    else:
        raise TypeError(type(data))

    if config:
        for key, val in config.items():
            text = text.replace(f"<{key}>", str(val))

    return text


def auto_translate(code: str, setter: callable, **config):
    MESSAGES.subscribe(lambda: setter(translate(code, **config)))


def vocalize(code: str, **config):
    message = translate(code, rand=True, config=config)
    VI.speak(message)
