
import functools
from typing import Dict, List

from wordle.config import SYMBOL_MATCH, SYMBOL_MISPLACED, SYMBOL_MISS

def load_words(filename: str) -> List[str]:
    with open(filename, "r", encoding="utf8") as file:
        words = file.read().splitlines()
        words = list(filter(lambda w: len(w) == 5, words))
    return words

def precompute_feedback(words: List[str], guesses: List[str]) -> Dict[str, Dict[str, str]]:
    feedback = dict()
    for word in words:
        feedback[word] = dict()
        for guess in guesses:
            feedback[word][guess] = evaluate_feedback(word, guess)
    return feedback

@functools.cache
def evaluate_feedback(word: str, guess: str) -> str:
    feedback = []
    word_indexes = {}
    for guess_index, guess_letter in enumerate(guess):
        if guess_letter == word[guess_index]:
            feedback.append(SYMBOL_MATCH)
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
                word_indexes[guess_letter] = word_index
                feedback.append(SYMBOL_MISPLACED)
                break
            word_index += 1
        else:
            # track the index out of bound, so that other istances of the same letter
            # will fail or succeed, respectively if misplaced or missing
            word_indexes[guess_letter] = word_index
            feedback.append(SYMBOL_MISS)

    return "".join(feedback)
