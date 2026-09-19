import heapq


class MedianStream:
    def __init__(self):
        self.lower = []
        self.higher = []

    def add(self, x: float):
        if len(self.lower) == len(self.higher):
            moved = heapq.heappushpop(self.higher, x)
            heapq.heappush(self.lower, -moved)
        else:
            moved = heapq.heappushpop(self.lower, -x)
            heapq.heappush(self.higher, -moved)

    def get_median(self):
        if len(self.lower) == len(self.higher):
            return (-self.lower[0] + self.higher[0]) / 2
        else:
            return -self.lower[0]
