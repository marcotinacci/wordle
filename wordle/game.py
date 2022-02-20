import random

from wordle.gameloader import load_words
from wordle.config import SYMBOL_MATCH, SYMBOL_MISPLACED, SYMBOL_MISS


class Wordle:
    def __init__(self, filename: str, secret: str = None):
        self.guesses = []
        self.feedback = []
        self.words = load_words(filename)
        self._secret = secret if secret is not None else random.choice(self.words)

    def guess(self, guess: str) -> str:
        self.guesses.append(guess)
        self.feedback.append(self.evaluate(guess))
        return self.feedback[-1]

    def evaluate(self, guess: str) -> str:
        feedback = ""
        for idx, letter in enumerate(guess):
            if letter == self._secret[idx]:
                feedback += SYMBOL_MATCH
            elif letter in self._secret:
                feedback += SYMBOL_MISPLACED
            else:
                feedback += SYMBOL_MISS
        return feedback

    def get_secret(self):
        return self._secret
