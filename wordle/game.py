import logging
import random
from pathlib import Path
from typing import *


# wordle game class
class Wordle:

    # feedback values
    MATCH: Final = "X"
    MISPLACED: Final = "?"
    MISS: Final = "-"

    MAX_ATTEMPTS: Final = 6

    def __init__(self, secret: str, filename: str):
        self.guesses = []
        self.feedback = []
        self.words = self._load_words(filename)
        self._secret = secret if secret is not None else random.choice(self.words)

    def guess(self, guess: str) -> str:
        self.guesses.append(guess)
        self.feedback.append(self.evaluate(guess))
        return self.feedback[-1]

    def evaluate(self, guess: str) -> str:
        feedback = ""
        for idx, letter in enumerate(guess):
            if letter == self._secret[idx]:
                feedback += self.MATCH
            elif letter in self._secret:
                feedback += self.MISPLACED
            else:
                feedback += self.MISS
        return feedback

    @staticmethod
    def _load_words(filename: str) -> List[str]:
        with open(filename, 'r') as file:
            words = file.read().splitlines()
            logging.debug("total words: %d", len(words))
            words = list(filter(lambda w: len(w) == 5, words))
            logging.debug("total 5 letters words: %d", len(words))
        return words


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    game = Wordle("house", Path(__file__).parent / "../data/words_cfreshman.txt")
    guess = "unity"
    feedback = game.guess(guess)
    logging.info("%s / %s = %s", game._secret, guess, feedback)
