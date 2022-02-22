import unittest

from wordle.game import Wordle
from wordle.utils import load_words


class TestGame(unittest.TestCase):

    def test_game(self):
        words = ["aaaaa", "bbbbb", "ccccc"]
        secret = "aaaaa"
        game = Wordle(words=words, secret=secret)
        self.assertEqual(game.get_secret(), secret)
        self.assertEqual(game.get_words(), words)

        feedback = game.evaluate("aaaaa")
        self.assertEqual(feedback, "XXXXX")

    def test_load_words(self):
        words = load_words("tests/words.txt")
        self.assertEqual(len(words), 5)
        self.assertTrue("crate" in words)
