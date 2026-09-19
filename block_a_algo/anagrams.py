import collections


def group_anagrams(words: list[str]) -> list[list[str]]:
    if not words:
        return []
    anagrams = collections.defaultdict(set)
    for word in words:
        if len(word) == 0:
            continue
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].add(word)
    return list(map(lambda x: list(x), anagrams.values()))


def group_anagrams2(words: list[str]) -> list[list[str]]:
    anagrams = collections.defaultdict(set)
    for word in words:
        freq = [0] * 26
        for ch in word:
            freq[ord(ch) - ord('a')] += 1
        anagrams[tuple(freq)].add(word)
    return list(map(lambda x: list(x), anagrams.values()))