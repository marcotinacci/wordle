import json
from typing import Dict, List
from os.path import exists

from wordle.config import SYMBOL_MATCH, MAX_ATTEMPTS
from wordle.strategy import Strategy, StrategyError
from wordle.strategy.utils import evaluate_feedback


class DecisionTree:
    def __init__(self, guess: str, choice: Dict[str, "DecisionTree"]):
        self.guess = guess
        self.choice = choice

    def to_dict(self) -> Dict[str, Dict]:
        return {
            "guess": self.guess,
            "choice": {
                feedback: tree.to_dict() if tree is not None else None
                for feedback, tree in self.choice.items()
            },
        }


def build_tree_from_dict(d: Dict) -> DecisionTree:
    guess = d["guess"]
    choice = {
        feedback: build_tree_from_dict(tree) if tree is not None else None
        for feedback, tree in d["choice"].items()
    }
    return DecisionTree(guess, choice)


def build_tree(
    strategy: Strategy, guesses: List[str], feedback: List[str]
) -> DecisionTree:
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
            continue
        guesses.append(g)
        feedback.append(f)
        tree = build_tree(strategy, guesses, feedback)
        if tree is not None:
            choice[f] = tree
        guesses.pop()
        feedback.pop()

    return DecisionTree(g, choice)


class PrecomputedStrategy(Strategy):
    def __init__(
        self,
        dictionary: List[str] = None,
        strategy: Strategy = None,
        filename: str = None,
    ):
        if strategy is not None and dictionary is not None:
            super().__init__(dictionary)
            self._decision_tree = build_tree(strategy, [], [])
            self._reset()
        elif filename is not None:
            super().__init__([])
            if not exists(filename):
                raise FileNotFoundError("file {} does not exist".format(filename))
            content = json.loads(open(filename, "r").read())
            self.dictionary = content["dictionary"]
            self._decision_tree = build_tree_from_dict(content["decision_tree"])
            self._reset()
        else:
            raise StrategyError("no strategy or filename given")

    def guess(self) -> str:
        return self._current_subtree.guess

    def set_history(self, guesses: List[str], feedback: List[str]):
        super().set_history(guesses, feedback)
        self._current_subtree = self._decision_tree
        for (g, f) in zip(guesses, feedback):
            if self._current_subtree.guess != g:
                raise StrategyError(
                    (f"guess {g} does not match precomputed guess "
                        f"{self._current_subtree.guess}")
                )
            self._current_subtree = self._current_subtree.choice[f]

    def update(self, guess: str, feedback: str):
        if guess != self._current_subtree.guess:
            raise StrategyError("guess does not match")
        if feedback not in self._current_subtree.choice:
            raise StrategyError("unexpected feedback %s", feedback)
        self._current_subtree = self._current_subtree.choice[feedback]

    def reset(self):
        super().reset()
        self._reset()

    def _reset(self):
        self._current_subtree = self._decision_tree

    def json(self) -> str:
        return json.dumps(
            {
                "decision_tree": self._decision_tree.to_dict(),
                "dictionary": self.dictionary,
            },
            indent=2,
            sort_keys=True,
        )
