class MinStack:
    def __init__(self):
        self.stack = []

    def push(self, x: int) -> None:
        current_min = x if not self.stack else min(x, self.stack[-1][1])
        self.stack.append((x, current_min))

    def pop(self) -> int:
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()[0]

    def top(self) -> int:
        if not self.stack:
            raise IndexError("top from empty stack")
        return self.stack[-1][0]

    def get_min(self) -> int:
        if not self.stack:
            raise IndexError("get_min from empty stack")
        return self.stack[-1][1]