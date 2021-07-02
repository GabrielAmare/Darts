from __future__ import annotations

from typing import List, Dict

__all__ = ["ActionHandler", "action_method"]


class action_method:
    __cache__: List[action_method] = []

    @classmethod
    def pop_cache(cls) -> Dict[str, callable]:
        cache = {am.name: am.method for am in cls.__cache__}
        cls.__cache__ = []
        return cache

    def __init__(self, method: callable):
        self.name: str = method.__name__
        self.method: callable = method


class ActionHandler:
    def __init_subclass__(cls, **kwargs):
        cls.__actions: Dict[str, callable] = action_method.pop_cache()

    def apply(self, name, *args, **kwargs):
        """
            Will call the method binded to the specified command type
        """
        if name in self.__actions:
            method = self.__actions[name]
            return method(self, *args, **kwargs)
        else:
            raise Exception(f"action method {name!r} not found")
