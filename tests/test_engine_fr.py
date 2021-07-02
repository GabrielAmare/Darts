import unittest

from darts.game_engine import engine_fr
from darts.commands import *
import os

os.chdir('..')


class TestEngineFr(unittest.TestCase):
    def test_commands(self):
        """Testing some (text -> command) return the correct object through the engine"""
        COMMANDS = {
            'quitter': Quit(),
            'ouvrir les paramètres': OpenSettings(),
            'ok': StartParty(),
            'annuler': Undo(),
            'refaire': Redo(),
            'annuler deux fois': Undo(times=2),
            'refaire 3 fois': Redo(times=3),
            'michel et patrick': AddPlayers(players=[O_Player(name='michel'), O_Player(name='patrick')]),
            '5 points pour michel': AddScore(scores=[O_Score(value=5, factor=1)], player=O_Player(name='michel')),
            'bull': AddScore(scores=[O_Score(value=25, factor=1)], player=None),
            '534': AddScore(scores=[O_Score(value=534, factor=1)], player=None),
            '301': SelectPartyType(name='301'),
            '501': SelectPartyType(name='501'),
            '801': SelectPartyType(name='801'),
            'cricket': SelectPartyType(name='cricket'),
            'molkky': SelectPartyType(name='molkky'),
        }

        for text, command in COMMANDS.items():
            result_command = engine_fr.read(text)
            self.assertEqual(command, result_command)


if __name__ == '__main__':
    unittest.main()
