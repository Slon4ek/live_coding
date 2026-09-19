class Queue:
    def __init__(self):
        self._in = []
        self._out = []

    def fill_out(self) -> None:
        if not self._out and self._in:
            while self._in:
                self._out.append(self._in.pop())

    def enqueue(self, x: int) -> None:
        self._in.append(x)

    def dequeue(self) -> int:
        self.fill_out()
        if not self._out:
            raise IndexError("dequeue from empty queue")
        return self._out.pop()

    def peek(self) -> int:
        self.fill_out()
        if not self._out:
            raise IndexError("peek from empty queue")
        return self._out[0]