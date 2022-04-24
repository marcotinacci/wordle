from typing import Callable, Dict, List

from wordle.strategy import Strategy, StrategyError


class HeuristicStrategy(Strategy):
    def __init__(self, dictionary: List[str]):
        super().__init__(dictionary)
        self._reset()

    def reset(self):
        super().reset()
        self._reset()
    
    def _reset(self):
        self.occurrences = build_occurrences(self.dictionary)
        self.candidates = sorted(
            self.dictionary,
            key=metric(self.occurrences),
            reverse=True,
        )

    def guess(self) -> str:
        if not self.candidates:
            raise StrategyError("no candidates left")
        return self.candidates[0]


def metric(occurrences: Dict[str, int]) -> Callable[[str], int]:
    def value(word: str) -> int:
        val = 0
        for letter in word:
            val += occurrences[letter]
        return val

    return value


def build_occurrences(words: List[str]) -> Dict[str, int]:
    occurrences = {}
    for word in words:
        for letter in set(word):
            if letter in occurrences:
                occurrences[letter] += 1
            else:
                occurrences[letter] = 1
    return occurrences
