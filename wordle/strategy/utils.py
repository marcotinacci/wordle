
from typing import List

from wordle.utils import evaluate_feedback


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
