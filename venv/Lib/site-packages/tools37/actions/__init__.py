from .Action import Action
from .Batch import Batch
from .ActionManager import ActionManager


class List:
    from .Append import Append
    from .Insert import Insert


class Dict:
    from .SetItem import SetItem  # TODO : make it handle list objects too


class Object:
    from .SetAttr import SetAttr
