import random

from wordle.gameloader import load_words
from wordle.player.utils import evaluate_feedback


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
        return evaluate_feedback(self._secret, guess)

    def get_secret(self):
        return self._secret
