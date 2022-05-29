import unittest
from unittest.mock import MagicMock

from wordle.config import MAX_ATTEMPTS
from wordle.game import Wordle
from wordle.player.player import Player
from wordle.strategy import Strategy, StrategyError


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.game = Wordle(words=["aaaaa", "bbbbb", "ccccc"], secret="aaaaa")
        self.strategy = Strategy([])
        self.strategy.guess = MagicMock(return_value="aaaaa")

    def test_player_error(self):
        with self.assertRaises(ValueError):
            Player(game=None, strategy=None)
        with self.assertRaises(ValueError):
            Player(game=self.game, strategy=None)
        with self.assertRaises(ValueError):
            Player(game=None, strategy=self.strategy)

    def test_player_wins(self):
        player = Player(game=self.game, strategy=self.strategy)
        guesses, _ = player.play()
        self.assertEqual(guesses[-1], self.game.get_secret())

    def test_player_loses(self):
        strategy = Strategy([])
        strategy.guess = MagicMock(return_value="bbbbb")
        player = Player(game=self.game, strategy=strategy)
        guesses, _ = player.play()
        self.assertNotEqual(guesses[-1], self.game)
        self.assertEqual(len(guesses), MAX_ATTEMPTS)

    def test_player_strategy_error(self):
        strategy = Strategy([])
        strategy.guess = MagicMock(side_effect=StrategyError("test"))
        player = Player(game=self.game, strategy=strategy)
        guesses, feedback = player.play()
        self.assertEqual(guesses, [])
        self.assertEqual(feedback, [])

    def test_player_guess(self):
        player = Player(game=self.game, strategy=self.strategy)
        guesses, feedback = player.play()
        self.assertEqual(guesses[0], "aaaaa")
