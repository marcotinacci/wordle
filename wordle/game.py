import random
from typing import List

from wordle.strategy.utils import evaluate_feedback


class Wordle:
    def __init__(self, words: List[str], secret: str = None):
        self._guesses = []
        self._feedback = []
        self._words = words
        self._secret = secret if secret is not None else random.choice(self._words)

    def evaluate(self, guess: str) -> str:
        return evaluate_feedback(self._secret, guess)

    def get_secret(self):
        return self._secret

    def get_words(self):
        return self._words
