from typing import TypeVar, Iterable, Iterator
import itertools

T = TypeVar("T")


def batched(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    if size <= 0:
        raise ValueError("size must be > 0")

    iterable = iter(iterable)

    while True:
        # batch = []
        # for _ in range(size):
        #     try:
        #         batch.append(next(iterable))
        #     except StopIteration:
        #         break
        batch = list(itertools.islice(iterable, size))
        if not batch:
            return
        yield batch
