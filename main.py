
from typing import *


def load_words(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        words = file.read().splitlines()
        # print("total words", len(words))
        words = list(filter(lambda w: len(w) == 5, words))
        # print("5 letters words", len(words))
    return words


def build_occurences(words: List[str]) -> Dict[str, int]:
    occurrences = dict()
    for word in words:
        for letter in set([letter for letter in word]):
            if letter in occurrences:
                occurrences[letter] += 1
            else:
                occurrences[letter] = 0
    return occurrences

def build_candidates(occurrences: Dict[str, int], words: List[str]) -> Tuple[List[str], List[int]]:
    return sorted(words, key=lambda w: value(occurrences, w), reverse=True), sorted([value(occurrences, w) for w in words], reverse=True)

def value(occurrences: Dict[str,int], word: str) -> int:
    v = 0
    for letter in word:
        v += occurrences[letter]
    return v

def filter_candidates(occurrences: Dict[str,int], candidates: List[str], attempts: List[str], feedback: List[str]) -> Tuple[List[str], List[int]]:
    for i in range(len(attempts)):
        candidates = list(filter(lambda w: predicate(w, attempts[i], feedback[i]), candidates))
    return candidates, sorted([value(occurrences, w) for w in candidates], reverse=True)

def predicate(word: str, attempt: str, feedback: str) -> bool:
    for i in range(len(word)):
        if feedback[i] == 'y' and word[i] != attempt[i]:
            return False
        if feedback[i] == 'n' and attempt[i] in word:
            return False
        # TODO check the logic of this step
        if feedback[i] == 'm' and attempt[i] not in word:
            return False
    return True

def filter_repeated_letters(occurrences: Dict[str,int], candidates: List[str]) -> Tuple[List[str], List[int]]:
    candidates = list(filter(lambda w: repeated(w), candidates))
    return candidates, sorted([value(occurrences, w) for w in candidates], reverse=True)

def repeated(word: str) -> bool:
    for i in range(len(word)):
        for j in range(i+1, len(word)):
            if word[i] == word[j]:
                return False
    return True


if __name__ == "__main__":
    attempts = ["arose","print"]
    feedback = ["nynnn","myynn"]
    words = load_words("words_octokatherine.txt")
    occurrences = build_occurences(words)
    # print("house : ", value(occurrences, "house"))
    # print("point : ", value(occurrences, "point"))
    candidates, values = build_candidates(occurrences, words)
    candidates, values = filter_candidates(occurrences, candidates, attempts, feedback)
    candidates, values = filter_repeated_letters(occurrences, candidates)

    print(candidates[:10])
    print(values[:10])
