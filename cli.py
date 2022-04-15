#!/usr/bin/env python

"""Console script for python_boilerplate."""
import logging
import sys
from pathlib import Path

from wordle.game import Wordle
from wordle.utils import load_words
from wordle.player.strategy import HeuristicStrategy, MinMaxStrategy
from wordle.player.player import Player


def main():
    """Console script for wordle."""
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    words = load_words(str(Path(__file__).parent / "data/words_cfreshman.txt"))

    secret = "offal"
    logging.info("heuristic strategy")
    player = Player(Wordle(words=words, secret=secret), HeuristicStrategy(words))
    player.play()
    logging.info("minmax strategy")
    player = Player(Wordle(words=words, secret=secret), MinMaxStrategy(words))
    player.play()
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
