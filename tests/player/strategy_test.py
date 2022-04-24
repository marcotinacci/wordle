import unittest

from wordle.config import DATA_ROOT
from wordle.strategy import Strategy, StrategyError
from wordle.strategy.heuristic_strategy import HeuristicStrategy
from wordle.strategy.minmax_strategy import MinMaxStrategy
from wordle.strategy.precomputed_strategy import PrecomputedStrategy
from wordle.utils import load_words

class TestStrategy(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.dictionary = load_words(DATA_ROOT / "dictionaries/words_test.txt")


    def test_strategy(self):
        s = Strategy(["aaaaa"])
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

    def test_minmax(self):
        words = ["abccc", "abbbb", "aaaaa"]
        s = MinMaxStrategy(words)
        self.assertEqual(s.candidates, words)

        guess = s.guess()
        self.assertEqual(guess, "abccc")

        s.update("abccc", "X____")
        self.assertEqual(s.candidates, ["aaaaa"])

        s.update("aaaaa", "XXXXX")
        
        s = MinMaxStrategy(words)
        s.update("aaaaa", "_____")
        self.assertEqual(s.candidates, [])
        with self.assertRaises(StrategyError):
            s.guess()

    def test_precomputed_heuristic(self):
        words = ["abccc", "abbbb", "aaaaa"]
        s = PrecomputedStrategy(words, HeuristicStrategy(words))

        self.assertEqual(s.dictionary, words)
        # NOTE precomputed strategies won't update candidates
        self.assertEqual(s.candidates, words)

        guess = s.guess()
        self.assertEqual(guess, "aaaaa")

        with self.assertRaises(StrategyError):
            s.update("ccccc", "X____")

        with self.assertRaises(StrategyError):
            s.update("aaaaa", "XX___")

        s.update("aaaaa", "X____")
        guess = s.guess()
        self.assertEqual(guess, "abbbb")

        s.update("abbbb", "XX___")
        guess = s.guess()
        self.assertEqual(guess, "abccc")

        s.reset()
        guess = s.guess()
        self.assertEqual(guess, "aaaaa")

