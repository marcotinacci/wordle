from typing import List

from wordle.strategy import Strategy, StrategyError
from wordle.strategy.utils import evaluate_feedback


class MinMaxStrategy(Strategy):

    def __init__(self, dictionary: List[str]):
        super().__init__(dictionary)
        self.reset()

    def guess(self) -> str:
        if not self.candidates:
            raise StrategyError("no candidates left")
        
        best_score = float("inf")
        best_guess = None
        for guess in self.candidates:
            counter = dict()
            for target in self.candidates:
                f = evaluate_feedback(target, guess)
                counter[f] = counter.setdefault(f, 0) + 1
                if counter[f] > best_score:
                    break
            score = max(counter.values())
            if score < best_score:
                best_score = score
                best_guess = guess

        return best_guess
