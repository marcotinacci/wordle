import logging
from typing import Callable, Dict, List, Tuple

from wordle.config import MAX_ATTEMPTS, SYMBOL_MATCH, SYMBOL_MISPLACED, SYMBOL_MISS
from wordle.game import Wordle


def predicate(word: str, guesses: List[str], feedback: List[str]) -> bool:
    """Return if the word is a valid candidate given the history of guesses
    and feedback."""

    for i, _ in enumerate(guesses):
        for j, letter in enumerate(word):
            if feedback[i][j] == SYMBOL_MATCH and letter != guesses[i][j]:
                return False
            if feedback[i][j] == SYMBOL_MISS and letter in guesses[i]:
                return False
            if feedback[i][j] == SYMBOL_MISPLACED and letter == guesses[i][j]:
                return False
    return True


def filter_candidates(
    candidates: List[str], guesses: List[str], feedback: List[str]
) -> List[str]:
    return list(filter(lambda w: predicate(w, guesses, feedback), candidates))


def build_occurrences(words: List[str]) -> Dict[str, int]:
    occurrences = {}
    for word in words:
        for letter in set(word):
            if letter in occurrences:
                occurrences[letter] += 1
            else:
                occurrences[letter] = 1
    return occurrences


def heuristic(occurrences: Dict[str, int]) -> Callable[[str], int]:
    def value(word: str) -> int:
        val = 0
        for letter in word:
            val += occurrences[letter]
        return val

    return value


class HeuristicPlayer:
    def __init__(self, game: Wordle):
        self.game = game
        self.occurrences = build_occurrences(self.game.words)
        self.candidates = sorted(
            self.game.words, key=heuristic(self.occurrences), reverse=True
        )

    def play(self) -> Tuple[List[str], List[str]]:
        guesses = []
        feedback = []
        for i in range(MAX_ATTEMPTS):

            if not len(self.candidates):
                logging.error("No candidates left")
                logging.info("Word not found: %s", self.game.get_secret())
                return guesses, feedback
            logging.debug("Candidates left: %d", len(self.candidates))

            best_guess = self.best_guess()

            guesses.append(best_guess)
            feedback.append(self.game.evaluate(best_guess))

            logging.info("guess %d: %s -> %s", i, best_guess, feedback[-1])

            if feedback[-1] == SYMBOL_MATCH * 5:
                logging.info("Found the word: %s", best_guess)
                return guesses, feedback

            # NOTE: the sorting by value is preserved after filtering
            self.candidates = filter_candidates(self.candidates, guesses, feedback)

        logging.info("Word not found: %s", self.game.get_secret())
        return guesses, feedback

    def best_guess(self):
        return self.candidates[0]
