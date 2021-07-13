from abc import ABC

from darts.base import DictInterface
from darts.base_events import Emitter


class BaseScore(Emitter, DictInterface, ABC):
    pass
