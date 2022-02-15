
import logging
from typing import *

from wordle.game import Wordle


def predicate(word: str, guesses: List[str], feedback: List[str]) -> bool:
    for i in range(len(guesses)):
        for j, letter in enumerate(word):
            if feedback[i][j] == Wordle.MATCH and letter != guesses[i][j]:
                return False
            if feedback[i][j] == Wordle.MISS and letter in guesses[i]:
                return False
            if feedback[i][j] == Wordle.MISPLACED and letter == guesses[i][j]:
                return False
    return True

def build_occurences(words: List[str]) -> Dict[str, int]:
    occurrences = dict()
    for word in words:
        for letter in set([letter for letter in word]):
            if letter in occurrences:
                occurrences[letter] += 1
            else:
                occurrences[letter] = 1
    return occurrences

def euristic(occurrences: Dict[str,int]) -> Callable[[str], int]:
    def value(word: str) -> int:
        v = 0
        for letter in word:
            v += occurrences[letter]
        return v
    return value

def filter_candidates(candidates: List[str], guesses: List[str], feedback: List[str]) -> List[str]:
    return list(filter(lambda w: predicate(w, guesses, feedback), candidates))


class EuristicPlayer:

    def __init__(self, game: Wordle):
        self.game = game
        self.occurrences = build_occurences(self.game.words)
        self.candidates = sorted(self.game.words, key=euristic(self.occurrences), reverse=True)

    def play(self):
        guesses = []
        feedback = []
        for i in range(self.game.MAX_ATTEMPTS):

            if not len(self.candidates):
                logging.error("No candidates left")
                return guesses, feedback
            else:
                logging.debug("Candidates left: %d", len(self.candidates))

            best_guess = self.candidates[0]
            guesses.append(best_guess)
            feedback.append(self.game.evaluate(best_guess))
            logging.info("guess %d: %s -> %s", i, best_guess, feedback[-1])
            if feedback[-1] == self.game.MATCH * 5:
                logging.info("Found the word: %s", best_guess)
                return guesses, feedback

            # NOTE: the sorting by value is preserved after filtering
            self.candidates = filter_candidates(self.candidates, guesses, feedback)

        logging.info("Found the word: %s", self.game._secret)
        return guesses, feedback

