import logging
from typing import Callable, Dict, List, Tuple

from wordle.config import MAX_ATTEMPTS, SYMBOL_MATCH, SYMBOL_MISPLACED, SYMBOL_MISS
from wordle.game import Wordle


def is_candidate(word: str, guesses: List[str], feedback: List[str]) -> bool:
    """Return if the word is a valid candidate given the history of guesses
    and feedback."""

    for i, guess in enumerate(guesses):

        # check SYMBOL_MATCH
        for j, letter in enumerate(word):
            if feedback[i][j] == SYMBOL_MATCH and letter != guess[j]:
                return False

        # check SYMBOL_MISPLACED and SYMBOL_MISS
        word_indexes = {}
        for guess_index, guess_letter in enumerate(guess):
            if feedback[i][guess_index] not in (SYMBOL_MISPLACED, SYMBOL_MISS):
                continue
            # check and set the letter index on the word
            if guess_letter not in word_indexes:
                word_indexes[guess_letter] = -1
            word_index = word_indexes[guess_letter] + 1

            # cycle on the word until we find a new misplaced match
            while word_index < len(word):
                if (
                    # check if letter is found
                    word[word_index] == guess_letter
                    # skip if in the same position
                    and word_index != guess_index
                    # check it's not another match
                    and guess[word_index] != guess_letter
                ):
                    if feedback[i][guess_index] == SYMBOL_MISPLACED:
                        word_indexes[guess_letter] = word_index
                        break
                    # else feedback element is SYMBOL_MISS
                    return False
                word_index += 1
            else:
                # if the match is not found feedback isn't compatible with the word
                if feedback[i][guess_index] == SYMBOL_MISPLACED:
                    return False
                # else feedback element is SYMBOL_MISS
                # track the index out of bound, so that other istances of the same letter
                # will fail or succeed, respectively if misplaced or missing
                word_indexes[guess_letter] = word_index

    return True


def filter_candidates(
    candidates: List[str], guesses: List[str], feedback: List[str]
) -> List[str]:
    return list(filter(lambda w: is_candidate(w, guesses, feedback), candidates))


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
