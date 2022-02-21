import unittest

from wordle.player.utils import evaluate_feedback, is_candidate


class TestStrategyMethods(unittest.TestCase):

    def test_evaluate_feedback(self):
        self.assertEqual(evaluate_feedback("house", "house"), "XXXXX")
        self.assertEqual(evaluate_feedback("house", "wrong"), "__?__")
        self.assertEqual(evaluate_feedback("abide", "speed"), "__?_?")
        self.assertEqual(evaluate_feedback("erase", "speed"), "?_??_")
        self.assertEqual(evaluate_feedback("steal", "speed"), "X_X__")
        self.assertEqual(evaluate_feedback("crepe", "speed"), "_?X?_")
        self.assertEqual(evaluate_feedback("pearl", "eerie"), "_X?__")
        self.assertEqual(evaluate_feedback("talon", "salsa"), "_XX__")

    def test_is_candidate(self):
        self.assertTrue(is_candidate("house", ["house"], ["XXXXX"]))
        self.assertFalse(is_candidate("house", ["wrong"], ["XXXXX"]))
        self.assertTrue(is_candidate("abide", ["speed"], ["__?_?"]))
        self.assertFalse(is_candidate("abide", ["speed"], ["__???"]))
        self.assertTrue(is_candidate("erase", ["speed"], ["?_??_"]))
        self.assertFalse(is_candidate("erase", ["speed"], ["?_?__"]))
        self.assertTrue(is_candidate("steal", ["speed"], ["X_X__"]))
        self.assertFalse(is_candidate("steal", ["speed"], ["X_X?_"]))
        self.assertTrue(is_candidate("crepe", ["speed"], ["_?X?_"]))
        self.assertFalse(is_candidate("crepe", ["speed"], ["_?X__"]))
        self.assertFalse(is_candidate("rinse", ["eerie"], ["????X"]))

    def test_is_candidate_history(self):
        self.assertTrue(is_candidate(
            word="tacit",
            guesses=["unity", "arose", "plait", "habit"],
            feedback=["__??_", "?____", "__?XX", "_X_XX"],
        ))
        self.assertFalse(is_candidate(
            word="tacit",
            guesses=["unity", "arose"],
            feedback=["__??_", "_____"],
        ))
        self.assertFalse(is_candidate(
            word="tacit",
            guesses=["arose", "unity"],
            feedback=["_____", "__??_"],
        ))

    def test_is_candidate_empty(self):
        self.assertTrue(is_candidate(
            word="tacit",
            guesses=[],
            feedback=[],
        ))