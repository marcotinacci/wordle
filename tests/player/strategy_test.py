import unittest

from wordle.player.strategy import HeuristicStrategy, Strategy, StrategyError


class TestStrategy(unittest.TestCase):

    def test_strategy(self):
        s = Strategy()
        self.assertEqual(s.guesses, [])
        self.assertEqual(s.feedback, [])

        with self.assertRaises(NotImplementedError):
            s.guess()

        s.update("aaaaa", "XXXXX")
        self.assertEqual(s.guesses, ["aaaaa"])
        self.assertEqual(s.feedback, ["XXXXX"])

    def test_heuristic(self):
        s = HeuristicStrategy(["abccc", "abbbb", "aaaaa"])
        self.assertEqual(s.occurrences, {"a": 3, "b": 2, "c": 1})
        self.assertEqual(s.candidates, ["aaaaa", "abbbb", "abccc"])

        guess = s.guess()
        self.assertEqual(guess, "aaaaa")

        s.update("aaaaa", "X____")
        self.assertEqual(s.candidates, ["abbbb", "abccc"])

        s.update("abbbb", "XXXXX")
        self.assertEqual(s.candidates, ["abbbb"])

        s = HeuristicStrategy(["abccc", "abbbb", "aaaaa"])
        s.update("aaaaa", "_____")
        self.assertEqual(s.candidates, [])
        with self.assertRaises(StrategyError):
            s.guess()
