import json
import unittest
from pathlib import Path

from wordle.strategy import Strategy, StrategyError
from wordle.strategy.heuristic_strategy import HeuristicStrategy
from wordle.strategy.minmax_strategy import MinMaxStrategy
from wordle.strategy.precomputed_strategy import (
    PrecomputedStrategy, DecisionTree, build_tree_from_dict, build_tree)
from wordle.utils import load_words

DATA_ROOT = Path(__file__).parent.parent / "data"


class TestStrategy(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.dictionary = load_words(DATA_ROOT / "words_test.txt")

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

        s.set_history(guesses=["aaaaa", "abbbb"], feedback=["X____", "XX___"])
        self.assertEqual(s.guess(), "abccc")

        with self.assertRaises(StrategyError) as cm:
            s.set_history(guesses=["zzzzz"], feedback=["_____"])

        self.assertEqual(
            cm.exception.args[0],
            "guess zzzzz does not match precomputed guess aaaaa")

    def test_precomputed_heuristic_from_file(self):
        filename = DATA_ROOT / "strategy_test.json"
        s = PrecomputedStrategy(filename=filename)

        self.assertEqual(s.dictionary, ["aaaaa", "abbbb", "aabbb"])
        self.assertEqual(s.guess(), "aaaaa")

        s.update("aaaaa", "X____")
        self.assertEqual(s.guess(), "abbbb")

    def test_precomputed_file_not_found(self):
        filename = DATA_ROOT / "doesnt_exist.json"
        with self.assertRaises(FileNotFoundError):
            PrecomputedStrategy(filename=filename)

    def test_non_existing_strategy(self):
        with self.assertRaises(StrategyError):
            PrecomputedStrategy()

    def test_decision_tree(self):
        tree = DecisionTree("aaaaa", {
            "X____": DecisionTree("abbbb", {}),
            "XX___": DecisionTree("aabbb", {}),
        })

        d = tree.to_dict()

        self.assertEqual(d, {
            "guess": "aaaaa",
            "choice": {
                "X____": {
                    "guess": "abbbb",
                    "choice": {},
                },
                "XX___": {
                    "guess": "aabbb",
                    "choice": {},
                },
            },
        })

    def test_build_tree(self):
        tree = build_tree(Strategy([]), ["aaaaa"] * 7, ["_____"] * 7)
        self.assertIsNone(tree)

    def test_build_tree_from_dict(self):
        d = {
            "guess": "aaaaa",
            "choice": {
                "X____": {
                    "guess": "abbbb",
                    "choice": {},
                },
                "XX___": {
                    "guess": "aabbb",
                    "choice": {},
                },
            },
        }

        tree = build_tree_from_dict(d)
        self.assertEqual(tree.guess, "aaaaa")
        self.assertEqual(tree.choice["X____"].guess, "abbbb")
        self.assertEqual(tree.choice["XX___"].guess, "aabbb")

    def test_save_precomputed_strategy(self):
        words = ["aabbb", "abbbb", "aaaaa"]
        s = PrecomputedStrategy(words, HeuristicStrategy(words))
        content = json.loads(s.json())

        self.assertEqual(content, {
            "dictionary": ["aabbb", "abbbb", "aaaaa"],
            "decision_tree": {
                "guess": "aaaaa",
                "choice": {
                    "X____": {
                        "guess": "abbbb",
                        "choice": {},
                    },
                    "XX___": {
                        "guess": "aabbb",
                        "choice": {},
                    },
                },
            },
        })
