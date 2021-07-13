import difflib
from tkinter import PhotoImage
from typing import List, TypeVar, Callable, Tuple, Iterator


def expr_match_ratio(expr1: str, expr2: str) -> float:
    return difflib.SequenceMatcher(isjunk=None, a=expr1, b=expr2).ratio()


E = TypeVar('E')
V = TypeVar('V')


def maximums_by(elements: Iterator[E], criteria: Callable[[E], V]) -> Tuple[V, List[E]]:
    max_elements = []
    max_value = None

    for element in elements:
        value = criteria(element)
        if max_value is None or value > max_value:
            max_value, max_elements = value, [element]
        elif value == max_value:
            max_elements.append(element)

    return max_value, max_elements


def is_int(o):
    return isinstance(o, int)


def is_str(o):
    return isinstance(o, str)


def resize_image(photo: PhotoImage, width: int, height: int) -> PhotoImage:
    return photo.subsample(photo.width() // width, photo.height() // height)


def rescale_image(photo: PhotoImage, scale: float) -> PhotoImage:
    return resize_image(photo, int(scale * photo.width()), int(scale * photo.height()))


def memorize(function):
    memory = {}

    def wrapped(*args, **kwargs):
        key = args, *kwargs.items()
        if key in memory:
            result = memory[key]
        else:
            result = memory[key] = function(*args, **kwargs)

        return result

    return wrapped
