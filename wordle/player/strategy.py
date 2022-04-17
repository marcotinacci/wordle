import logging
from typing import Dict, List, Callable
from progress.bar import Bar

from wordle.player.utils import evaluate_feedback, filter_candidates, precompute_feedback


class Strategy:
    def __init__(self):
        self.setup()

    def setup(self):
        self.guesses = []
        self.feedback = []

    def guess(self) -> str:
        raise NotImplementedError

    def update(self, guess: str, feedback: str):
        self.guesses.append(guess)
        self.feedback.append(feedback)

    @staticmethod
    def evaluate_feedback(word: str, guess: str) -> str:
        return evaluate_feedback(word, guess)


class PrecomputedStrategy(Strategy):

    class DecisionTree:
        def __init__(self, guess: str, choice: Dict[str, "PrecomputedStrategy.DecisionTree"]):
            self.guess = guess
            self.choice = choice

    @staticmethod
    def _precompute(words: List[str], strategy: Strategy) -> DecisionTree:
        logging.info("precomputing %s", strategy.__class__.__name__)
        # tree root
        guess = strategy.guess()
        choice = dict()
        with Bar(strategy.__class__.__name__, max=len(words)) as bar:
            for target in words:
                feedback = evaluate_feedback(target, guess)
                # TODO implement strategy.run instead
                strategy.setup()
                strategy.update(guess, feedback)
                choice[feedback] = PrecomputedStrategy.DecisionTree(
                    strategy.guess(), dict()
                )
                bar.next()
        return PrecomputedStrategy.DecisionTree(guess, choice)

    def __init__(self, words: List[str], strategy: Strategy):
        super().__init__()
        self._decision_tree = self._precompute(words, strategy)

    def guess(self) -> str:
        if self._decision_tree is None:
            raise StrategyError("no options available")
        return self._decision_tree.guess
    
    def update(self, guess: str, feedback: str):
        if guess != self._decision_tree.guess:
            raise StrategyError("guess does not match")
        if feedback not in self._decision_tree.choice:
            raise StrategyError("unexpected feedback %s", feedback)
        self._decision_tree = self._decision_tree.choice[feedback]


class HeuristicStrategy(Strategy):

    def __init__(self, words: List[str]):
        self.words = words
        Strategy.__init__(self)

    def setup(self):
        super().setup()
        self.occurrences = HeuristicStrategy.build_occurrences(self.words)
        self.candidates = sorted(
            self.words,
            key=HeuristicStrategy.metric(self.occurrences), reverse=True
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


class MinMaxStrategy(Strategy):

    def __init__(self, words: List[str]):
        self.words = words
        Strategy.__init__(self)

    def setup(self):
        super().setup()

        self.candidates = self.words[:]

    def guess(self) -> str:
        if not self.candidates:
            raise StrategyError("No candidates left")
        
        best_score = float("inf")
        best_guess = None
        for guess in self.candidates:
            counter = dict()
            for target in self.candidates:
                f = self.evaluate_feedback(target, guess)
                counter[f] = counter.setdefault(f, 0) + 1
                if counter[f] > best_score:
                    break
            score = max(counter.values())
            if score < best_score:
                best_score = score
                best_guess = guess

        return best_guess

    def update(self, guess: str, feedback: str):
        Strategy.update(self, guess, feedback)

        self.candidates = filter_candidates(
            self.candidates, self.guesses, self.feedback
        )

    def evaluate_feedback(self, word: str, guess: str) -> str:
        if hasattr(self, "feedback_matrix"):
            return self.feedback_matrix[word][guess]
        return evaluate_feedback(word, guess)



class StrategyError(Exception):
    pass
