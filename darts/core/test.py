import unittest
from darts import core


class TestParty(unittest.TestCase):
    def test_001(self):
        commands = [
            core.AddPlayer()
        ]

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
