from typing import Callable, Dict, List

from wordle.player.utils import filter_candidates


class Strategy:
    def __init__(self):
        self.guesses = []
        self.feedback = []

    def guess(self) -> str:
        raise NotImplementedError

    def update(self, guess: str, feedback: str):
        self.guesses.append(guess)
        self.feedback.append(feedback)


class HeuristicStrategy(Strategy):
    def __init__(self, words: List[str]):
        Strategy.__init__(self)
        self.occurrences = HeuristicStrategy.build_occurrences(words)
        self.candidates = sorted(
            words, key=HeuristicStrategy.metric(self.occurrences), reverse=True
        )

    def guess(self) -> str:
        if not self.candidates:
            raise StrategyError("No candidates left")
        return self.candidates[0]

    def update(self, guess: str, feedback: str):
        Strategy.update(self, guess, feedback)

        # NOTE: the order is preserved after filtering
        self.candidates = filter_candidates(
            self.candidates, self.guesses, self.feedback
        )

    @staticmethod
    def metric(occurrences: Dict[str, int]) -> Callable[[str], int]:
        def value(word: str) -> int:
            val = 0
            for letter in word:
                val += occurrences[letter]
            return val

        return value

    @staticmethod
    def build_occurrences(words: List[str]) -> Dict[str, int]:
        occurrences = {}
        for word in words:
            for letter in set(word):
                if letter in occurrences:
                    occurrences[letter] += 1
                else:
                    occurrences[letter] = 1
        return occurrences


class StrategyError(Exception):
    pass
