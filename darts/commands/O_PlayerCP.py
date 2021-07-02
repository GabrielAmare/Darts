from .O_Player import O_Player


class O_PlayerCP(O_Player):
    def __init__(self, name1: str, name2: str):
        super().__init__(name1 + " " + name2)
