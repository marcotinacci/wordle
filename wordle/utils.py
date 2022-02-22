import logging
from typing import List


def load_words(filename: str) -> List[str]:
    with open(filename, "r", encoding="utf8") as file:
        words = file.read().splitlines()
        logging.debug("total words: %d", len(words))
        words = list(filter(lambda w: len(w) == 5, words))
        logging.debug("total 5 letters words: %d", len(words))
    return words
