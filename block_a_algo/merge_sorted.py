import heapq
from typing import Iterable, Iterator


def merge_sorted(iterables: list[Iterable[int]]) -> Iterator[int]:
    #yield from heapq.merge(*iterables)
    heap = []
    for idx, it in enumerate(iterables):
        iter_it = iter(it)
        try:
            first = next(iter_it)
            heapq.heappush(heap, (first, idx, iter_it))
        except StopIteration:
            pass

    last, seen = None, False
    while heap:
        current, idx, it = heapq.heappop(heap)
        if not seen or current != last:
            yield current
            last = current
            seen = True
        try:
            next_item = next(it)
            heapq.heappush(heap, (next_item, idx, it))
        except StopIteration:
            pass
