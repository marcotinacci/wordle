from typing import List

from wordle.strategy.utils import filter_candidates


class Strategy:
    def __init__(self, dictionary: List[str]):
        self.dictionary = dictionary
        self.candidates = self.dictionary
        self.guesses = []
        self.feedback = []
        self._filter_candidates()

    def guess(self) -> str:
        raise NotImplementedError

    def reset(self):
        self.candidates = self.dictionary
        self.set_history([], [])

    def update(self, guess: str, feedback: str):
        self.guesses.append(guess)
        self.feedback.append(feedback)
        self._filter_candidates()

    def set_history(self, guesses: List[str], feedback: List[str]):
        self.guesses = guesses
        self.feedback = feedback
        self._filter_candidates()

    def _filter_candidates(self):
        self.candidates = filter_candidates(
            self.candidates, self.guesses, self.feedback
        )


class StrategyError(Exception):
    pass
