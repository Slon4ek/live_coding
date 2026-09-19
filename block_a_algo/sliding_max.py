import collections


def sliding_max(nums: list[int], k: int) -> list[int]:
    if k <= 0:
        raise ValueError("k must be > 0")
    if k > len(nums):
        raise ValueError("k must be <= len(nums)")

    result = []
    window = collections.deque()
    for i in range(len(nums)):
        while window and nums[window[-1]] <= nums[i]:
            window.pop()
        window.append(i)
        if i >= k - 1:
            result.append(nums[window[0]])
    return result