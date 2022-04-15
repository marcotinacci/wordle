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
from wordle.player.strategy import HeuristicStrategy, MinMaxStrategy, Strategy
from wordle.player.player import Player


def main():
    """Console script for wordle."""
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    words = load_words(str(Path(__file__).parent / "data/words_cfreshman.txt"))

    words = words[0:10000:100]
    print(words)
    simulation(HeuristicStrategy, words)
    simulation(MinMaxStrategy, words)
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
