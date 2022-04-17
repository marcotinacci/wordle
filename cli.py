#!/usr/bin/env python

"""Console script for python_boilerplate."""
import logging
import sys
from pathlib import Path
from progress.bar import Bar
from time import time
from typing import List

from wordle.game import Wordle
from wordle.utils import load_words
from wordle.player.strategy import HeuristicStrategy, MinMaxStrategy, PrecomputedStrategy, Strategy
from wordle.player.player import Player
from wordle.player.utils import precompute_feedback


def main():
    """Console script for wordle."""
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    words = load_words(str(Path(__file__).parent / "data/words_cfreshman.txt"))

    # logging.info("precomputing feedback")
    # MinMaxStrategy.feedback_matrix = precompute_feedback(words, words)

    # words = words[:100]
    strategy = PrecomputedStrategy(words, MinMaxStrategy(words))

    print(strategy._decision_tree.guess)
    print(strategy._decision_tree.choice.keys())

    for secret in words:
        player = Player(Wordle(words=words, secret=secret), strategy)
        start = time()
        guesses, feedback = player.play()
        execution_time = time() - start
        result = {
            "secret": secret,
            "guesses": guesses,
            "feedback": feedback,
            "execution_time": execution_time,
        }
        print(result)

    # simulation(HeuristicStrategy, words)
    # simulation(MinMaxStrategy, words)
    return 0

def simulation(strategy: Strategy, words: List[str]):
    logging.info("strategy simulation: %s", strategy.__name__)
    
    with Bar(strategy.__name__, max=len(words)) as bar:
        results = []
        for secret in words:
            player = Player(Wordle(words=words, secret=secret), strategy(words))
            start = time()
            guesses, feedback = player.play()
            execution_time = time() - start
            results.append({
                "secret": secret,
                "guesses": guesses,
                "feedback": feedback,
                "execution_time": execution_time,
            })
            bar.next()

    logging.info("average execution time: %f", sum(r["execution_time"] for r in results) / len(results))
    logging.info("average guesses: %f", sum(len(r["guesses"]) for r in results) / len(results))

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
