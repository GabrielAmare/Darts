import unittest

from darts.core.engines import ENGINES
from darts.core.commands import *
import os

os.chdir('..')


class TestEngineFr(unittest.TestCase):
    def test_commands(self):
        """Testing some (text -> command) return the correct object through the engine"""
        COMMANDS = {
            'quitter': Quit(),
            'ouvrir les paramètres': OpenSettings(),
            'menu principal': MainMenu(),
            'ok': StartParty(),
            'annuler': Undo(),
            'refaire': Redo(),
            'annuler deux fois': Undo(times=2),
            'refaire 3 fois': Redo(times=3),
            'michel': AddPlayer(player=PlayerName(name='michel')),
            'jean-michel': AddPlayer(player=PlayerName(name='jean michel')),
            'michel et patrick': AddPlayers(players=[PlayerName(name='michel'), PlayerName(name='patrick')]),
            '5 points pour michel': AddScore(scores=[ScoreValue(value=5, factor=1)], player=PlayerName(name='michel')),
            'bull': AddScore(scores=[ScoreValue(value=25, factor=1)], player=None),
            '534': AddScore(scores=[ScoreValue(value=534, factor=1)], player=None),
            'X 7': AddScore(scores=[ScoreValue(value=17, factor=1)], player=None),
            '238 points': AddScore(scores=[ScoreValue(value=238, factor=1)], player=None),
            'triple 19': AddScore(scores=[ScoreValue(value=19, factor=3)], player=None),
            '301': SelectPartyType(name='301'),
            '501': SelectPartyType(name='501'),
            '801': SelectPartyType(name='801'),
            'cricket': SelectPartyType(name='cricket'),
            'molkky': SelectPartyType(name='molkky'),
            'around the clock': SelectPartyType(name='around the clock'),
        }

        for text, command in COMMANDS.items():
            result_command = ENGINES['fr'].read(text)
            self.assertEqual(command, result_command)


if __name__ == '__main__':
    unittest.main()
