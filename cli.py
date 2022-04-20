#!/usr/bin/env python

import logging
import sys
from pathlib import Path
from progress.bar import Bar
from time import time
from typing import List

from wordle.game import Wordle
from wordle.utils import load_words
from wordle.strategy import Strategy, StrategyError
from wordle.strategy.heuristic_strategy import HeuristicStrategy
from wordle.strategy.minmax_strategy import MinMaxStrategy
from wordle.strategy.precomputed_strategy import PrecomputedStrategy
from wordle.player.player import Player


def main():
    """Console script for wordle."""
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    words = load_words(str(Path(__file__).parent / "data/words_cfreshman.txt"))

    simulation(PrecomputedStrategy(words, HeuristicStrategy(words)), words)
    simulation(HeuristicStrategy(words), words)
    simulation(MinMaxStrategy(words), words)
    return 0

def simulation(strategy: Strategy, words: List[str]):
    logging.info("strategy simulation: %s", strategy.__class__.__name__)

    results = []
    with Bar(strategy.__class__.__name__, max=len(words)) as bar:
        for secret in words:
            player = Player(Wordle(words=words, secret=secret), strategy)
            start = time()
            try:
                guesses, feedback = player.play()
            except StrategyError as se:
                results.append({
                    "secret": secret,
                    "status": "error",
                    "message": str(se),
                })
                continue
            finally:
                bar.next()
            execution_time = time() - start
            player.strategy.reset()
            results.append({
                "secret": secret,
                "guesses": guesses,
                "feedback": feedback,
                "execution_time": execution_time,
                "status": "complete",
            })

    logging.info("average execution time: %f", sum(r["execution_time"] for r in results if r["status"] == "complete" ) / len(results))
    logging.info("average guesses: %f", sum(len(r["guesses"]) for r in results if r["status"] == "complete") / len(results))
    logging.info("number of errors: %d", len([r for r in results if r["status"] == "error"]))

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
