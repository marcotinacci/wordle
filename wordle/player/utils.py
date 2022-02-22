from typing import List

from wordle.config import SYMBOL_MATCH, SYMBOL_MISPLACED, SYMBOL_MISS


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


def is_candidate(word: str, guesses: List[str], feedback: List[str]) -> bool:
    """Return if the word is a valid candidate given the history of guesses
    and feedback."""

    for i, guess in enumerate(guesses):
        if evaluate_feedback(word, guess) != feedback[i]:
            return False
    return True

def filter_candidates(
    candidates: List[str], guesses: List[str], feedback: List[str]
) -> List[str]:
    return list(filter(lambda word: is_candidate(word, guesses, feedback), candidates))
