#!/usr/bin/env python

import logging
import sys
from time import time
from typing import List

import click
from progress.bar import Bar
from tabulate import tabulate

from wordle.config import DATA_ROOT, LOG_LEVEL, MAX_ATTEMPTS
from wordle.game import Wordle
from wordle.player.player import Player
from wordle.strategy import Strategy, StrategyError
from wordle.strategy.heuristic_strategy import HeuristicStrategy
from wordle.strategy.minmax_strategy import MinMaxStrategy
from wordle.strategy.precomputed_strategy import PrecomputedStrategy
from wordle.utils import load_words


@click.group()
def cli():
    pass


@cli.command()
@click.option("--secret", "-s", help="Secret word.")
@click.option("--strategy", "-S", default="heuristic", help="Strategy type to use.")
@click.option(
    "--dictionary", "-d", default="words_cfreshman.txt", help="Dictionary file."
)
@click.option(
    "--precomputed",
    "-p",
    is_flag=True,
    show_default=True,
    default=False,
    help="Load a precomputed strategy.",
)
def run(dictionary: str, secret: str, strategy: str, precomputed: bool) -> int:
    logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL)
    words = load_words(DATA_ROOT / "dictionaries" / dictionary)
    game = Wordle(words=words, secret=secret) if secret else Wordle(words=words)
    try:
        strategy = select_strategy(strategy, words, precomputed)
        player = Player(game, strategy)
        guesses, feedback = player.play()
    except (ValueError, StrategyError) as e:
        logging.error(e)
        return 1
    for i, (g, f) in enumerate(zip(guesses, feedback)):
        print("guess %d: %s => %s" % (i + 1, g, f))
    return 0


def select_strategy(strategy: str, words: List[str], precomputed: bool) -> Strategy:
    if precomputed:
        PrecomputedStrategy(
            filename=DATA_ROOT / "strategies" / "{}.json".format(strategy)
        )
    if strategy == "heuristic":
        return HeuristicStrategy(words)
    elif strategy == "minmax":
        return MinMaxStrategy(words)
    else:
        raise ValueError("unknown strategy: %s" % strategy)


@cli.command()
@click.argument("filename", type=str)
@click.option("--strategy", "-S", default="heuristic", help="Strategy type to use.")
@click.option(
    "--dictionary", "-d", default="words_cfreshman.txt", help="Dictionary file."
)
def precompute(filename: str, strategy: str, dictionary: str) -> int:
    logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL)
    words = load_words(DATA_ROOT / "dictionaries" / dictionary)
    try:
        strategy = select_strategy(strategy, words, False)
        precomputed_strategy = PrecomputedStrategy(words, strategy)
    except StrategyError as e:
        logging.error(e)
        return 1
    
    with open(DATA_ROOT / "strategies" / "{}.json".format(filename), "w") as f:
        f.write(precomputed_strategy.json(), 'w')

    return 0


@cli.command()
@click.argument("history", type=str, nargs=-1)
@click.option("--strategy", "-S", default="heuristic", help="Strategy type to use.")
@click.option(
    "--dictionary", "-d", default="words_cfreshman.txt", help="Dictionary file."
)
@click.option(
    "--precomputed",
    "-p",
    is_flag=True,
    show_default=True,
    default=False,
    help="Load a precomputed strategy.",
)
def play(history: List[str], strategy: str, dictionary: str, precomputed: bool) -> int:
    logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL)

    rounds = len(history) / 2
    if rounds > MAX_ATTEMPTS or len(history) % 2 != 0:
        logging.error("arguments must be <= 2 * %d", MAX_ATTEMPTS)
        return 1

    guesses = [g for i, g in enumerate(history) if i % 2 == 0]
    feedback = [f for i, f in enumerate(history) if i % 2 == 1]
    words = load_words(DATA_ROOT / "dictionaries" / dictionary)
    try:
        strategy = select_strategy(strategy, words, precomputed)
        strategy.set_history(guesses, feedback)
        print("hint: {}".format(strategy.guess()))
    except (ValueError, StrategyError) as e:
        logging.error(e)
        return 1
    return 0

@cli.command()
@click.argument("strategy", type=str)
@click.option("--sample", "-n", type=int, default=100, help="Sample size.")
@click.option(
    "--dictionary", "-d", default="words_cfreshman.txt", help="Dictionary file."
)
@click.option(
    "--precomputed",
    "-p",
    is_flag=True,
    show_default=True,
    default=False,
    help="Run precomputed strategies.",
)
def benchmark(strategy: str, sample: int, dictionary: str, precomputed: bool) -> int:

    logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL)

    words = load_words(DATA_ROOT / "dictionaries" / dictionary)[:sample]

    strategy = select_strategy(strategy, words, precomputed)
    results = []
    with Bar(strategy.__class__.__name__, max=len(words)) as bar:
        for secret in words:
            player = Player(Wordle(words=words, secret=secret), strategy)
            start = time()
            try:
                guesses, feedback = player.play()
            except StrategyError as se:
                results.append(
                    {
                        "secret": secret,
                        "status": "error",
                        "message": str(se),
                    }
                )
                continue
            finally:
                bar.next()
            execution_time = time() - start
            player.strategy.reset()
            results.append(
                {
                    "secret": secret,
                    "guesses": guesses,
                    "feedback": feedback,
                    "execution_time": execution_time,
                    "status": "complete",
                }
            )

    complete_records = len([r for r in results if r["status"] == "complete"])
    if complete_records == 0:
        print("There are no complete records")
        return 0

    print(
        tabulate(
            [
                ["metric", "value"],
                [
                    "avg time",
                    sum(
                        r["execution_time"]
                        for r in results
                        if r["status"] == "complete"
                    )
                    / len([r for r in results if r["status"] == "complete"]),
                ],
                [
                    "avg guesses",
                    sum(len(r["guesses"]) for r in results if r["status"] == "complete")
                    / len([r for r in results if r["status"] == "complete"]),
                ],
                [
                    "errors number",
                    len([r for r in results if r["status"] == "error"]),
                ],
            ],
            headers="firstrow",
            tablefmt="grid",
        )
    )


if __name__ == "__main__":
    cli()
