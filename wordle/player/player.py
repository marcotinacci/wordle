
import logging
from typing import List, Tuple

from wordle.config import MAX_ATTEMPTS, SYMBOL_MATCH
from wordle.game import Wordle
from wordle.player.strategy import Strategy, StrategyError


class Player:
    def __init__(self, game: Wordle, strategy: Strategy):
        self.game = game
        self.strategy = strategy

    def play(self) -> Tuple[List[str], List[str]]:
        guesses = []
        feedback = []
        for i in range(MAX_ATTEMPTS):

            try:
                g = self.strategy.guess()
            except StrategyError as e:
                logging.error(e)
                break
            fb = self.game.evaluate(g)

            guesses.append(g)
            feedback.append(fb)

            logging.info("guess %d: %s -> %s", i, g, fb)

            if fb == SYMBOL_MATCH * 5:
                logging.info("Found the word: %s", g)
                return guesses, feedback
            
            self.strategy.update(g, fb)
            pass

        logging.info("Word not found: %s", self.game.get_secret())
        return guesses, feedback

    def guess(self):
        return self.strategy.guess()
