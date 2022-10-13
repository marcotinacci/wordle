# Wordle

![tests](https://github.com/marcotinacci/wordle/actions/workflows/wordle.yml/badge.svg)
[![codecov](https://codecov.io/gh/marcotinacci/wordle/branch/main/graph/badge.svg?token=SJHIT1IBCY)](https://codecov.io/gh/marcotinacci/wordle)
![GitHub](https://img.shields.io/github/license/marcotinacci/wordle)

Python implementation of a [Wordle](https://en.wikipedia.org/wiki/Wordle) player.
The source code provides a structure to easily create Wordle players, and some built-in
strategies:
 * `heuristic`: a simple heuristic strategy that priorities words that contain letters
    with the highest frequency. Linear time complexity $O(W)$.
 * `minmax`: minmax strategy that minimize the maximum number of candidates on
the next move. Quadratic time complexity $O(W^2)$.
 * `precomputed`: _decorator_ strategy that precomputes the full decision tree. Constant
 time complexity $O(1)$ at runtime. Precomputation complexity is the same as the
 targeted strategy, as it is repeated for each step of the decision tree which has
 a constant number of nodes.

## Installation

Clone the repository and run the following command from the project root to install the
required dependencies (use a virtual environment if you wish, or don't, I'm not your
mother):

```bash
pip install -r requirments.txt
```

## Usage

The package provides a CLI interface to play with the different functions. Check the
help for more information in this way:

```bash
$ python cli.py --help
```

The main subcommand is `play`, that let you play with the different strategies:

```bash
$ python cli.py play
```

Here an example of a game with the `minmax` strategy:

```bash
$ python cli.py play -S minmax -p
hint: arise
$ python cli.py play -S minmax -p arise .____
hint: candy
$ python cli.py play -S minmax -p arise .____ candy _X__.
hint: bayou
```

`-S` let you choose the strategy to use. The default strategy is `heuristic`.

`-p` grabs the strategy from the precomputed tree named
    `data/strategies/<strategy-name>.json`.

Finally you need to provide the sequence of guess/feedback pairs, where the feedback is
encoded as a string of the following characters:
* `_`: incorrect letter
* `.`: correct letter, wrong position
* `X`: correct letter, correct position

# Acknowledgments

Thanks to @lostella for the always constructive conversations (that I'm missing), and to @davideboschetto and @albertoguiggiani for the laughs. 
