from distutils.command.build import build
import logging
from progress.bar import Bar
from typing import Dict, List

from wordle.config import SYMBOL_MATCH, MAX_ATTEMPTS
from wordle.strategy import Strategy, StrategyError
from wordle.strategy.utils import evaluate_feedback


class DecisionTree:
    def __init__(self, guess: str, choice: Dict[str, "DecisionTree"]):
        self.guess = guess
        self.choice = choice


def build_tree(strategy: Strategy, guesses: List[str], feedback: List[str]) -> DecisionTree:
    if len(guesses) > MAX_ATTEMPTS:
        return None
    choice = dict()
    strategy.reset()
    strategy.set_history(guesses, feedback)
    g = strategy.guess()
    for target in strategy.candidates:
        f = evaluate_feedback(target, g)
        if f in choice:
            continue
        if f == SYMBOL_MATCH * 5:
            choice[f] = None
            continue
        guesses.append(g)
        feedback.append(f)
        choice[f] = build_tree(strategy, guesses, feedback)
        guesses.pop()
        feedback.pop()

    return DecisionTree(g, choice)

class PrecomputedStrategy(Strategy):

    def __init__(self, dictionary: List[str], strategy: Strategy):
        super().__init__(dictionary)
        logging.info("start build_tree")
        self._decision_tree = build_tree(strategy, [], [])
        logging.info("end build_tree")

    def guess(self) -> str:
        if self._decision_tree is None:
            raise StrategyError("no options available")
        
        tree = self._decision_tree
        for (g, f) in zip(self.guesses, self.feedback):
            if tree.guess != g:
                raise StrategyError(
                    "guess %s does not match precomputed guess %s",
                    tree.guess, 
                    g,
                )
            tree = tree.choice[f]
        return tree.guess

    def update(self, guess: str, feedback: str):
        if guess != self._decision_tree.guess:
            raise StrategyError("guess does not match")
        if feedback not in self._decision_tree.choice:
            raise StrategyError("unexpected feedback %s", feedback)
        self._decision_tree = self._decision_tree.choice[feedback]
