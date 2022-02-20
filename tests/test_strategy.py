import unittest

from wordle.player.heuristic import predicate


class TestStrategyMethods(unittest.TestCase):

    def test_predicate(self):
        self.assertTrue(predicate("house", ["house"], ["XXXXX"]))
        self.assertTrue(predicate("abide", ["speed"], ["__???"]))
        self.assertFalse(predicate("abide", ["speed"], ["__?_?"]))
        # self.assertTrue(predicate("erase", ["speed"], ["?_??_"]))
        # self.assertFalse(predicate("erase", ["speed"], ["?_?__"]))
        # self.assertTrue(predicate("steal", ["speed"], ["X_X__"]))
        # self.assertFalse(predicate("steal", ["speed"], ["X_X?_"]))
        # self.assertTrue(predicate("crepe", ["speed"], ["_?X?_"]))
        # self.assertFalse(predicate("crepe", ["speed"], ["_?X__"]))
