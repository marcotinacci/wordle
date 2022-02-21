#!/usr/bin/env python

"""Console script for python_boilerplate."""
import logging
import sys
from pathlib import Path

from wordle.game import Wordle
from wordle.player.strategy import HeuristicStrategy
from wordle.player.player import Player


def main():
    """Console script for wordle."""
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    game = Wordle(filename=str(Path(__file__).parent / "data/words_cfreshman.txt"))
    player = Player(game, HeuristicStrategy(game.words))
    player.play()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
