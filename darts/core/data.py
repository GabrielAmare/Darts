from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Score:
    pass


@dataclass
class Player:
    name: str
    scores: List[Score]


@dataclass
class Party:
    players: List[Player]
    start: bool
    over: bool
    winner: Optional[Player]


from tools37 import CommandManager, bind_to, ActionManager
from tools37.actions import Object as AObject, List as AList, Dict as ADict, Batch
from . import commands as C


@dataclass
class AppCommandManager(CommandManager):
    party: Optional[Party]
    action_manager: ActionManager = ActionManager()

    @bind_to(C.MainMenu)
    def MainMenu(self, command: C.MainMenu):
        Object.SetAttr(obj=self.party, key=, val=)

    @bind_to(C.OpenSettings)
    def OpenSettings(self, command: C.OpenSettings):
        pass

    @bind_to(C.Quit)
    def Quit(self, command: C.Quit):
        pass

    @bind_to(C.StartParty)
    def StartParty(self, command: C.StartParty):
        pass

    @bind_to(C.AdjustMic)
    def AdjustMic(self, command: C.AdjustMic):
        pass

    @bind_to(C.Redo)
    def Redo(self, command: C.Redo):
        pass

    @bind_to(C.SelectPartyType)
    def SelectPartyType(self, command: C.SelectPartyType):
        pass

    @bind_to(C.SetLang)
    def SetLang(self, command: C.SetLang):
        pass

    @bind_to(C.Undo)
    def Undo(self, command: C.Undo):
        pass

    @bind_to(C.AddPlayer)
    def AddPlayer(self, command: C.AddPlayer):
        player = Player(
            name=command.player.name,
            scores=[]
        )
        initial_score = Score()

        action = Batch(
            AList.Append(
                obj=self.party.players,
                item=player
            ),
            AList.Append(
                obj=player.scores,
                item=initial_score
            )

        )
        self.action_manager.do()

    @bind_to(C.AddPlayers)
    def AddPlayers(self, command: C.AddPlayers):
        pass

    @bind_to(C.AddScore)
    def AddScore(self, command: C.AddScore):
        pass
