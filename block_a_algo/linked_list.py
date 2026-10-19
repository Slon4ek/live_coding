class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def has_cycle(self, head: ListNode | None) -> bool:
        """
        Определяет есть ли цикл в связном списке
        """
        if not head or not head.next:
            return False
        s = f = head
        while f and f.next:
            s = s.next
            f = f.next.next
            if s == f:
                return True
        return False

    def reverse_list(self, head: ListNode | None) -> ListNode | None:
        """
        Разворачивает связный список
        """
        prev = None
        cur = head
        while cur:
            next_node = cur.next
            cur.next = prev
            prev = cur
            cur = next_node
        return prev

    def is_palindrome(self, head: ListNode | None) -> bool:
        """
        Определяет является ли список палиндромом.
        """
        slow = fast = head

        if not slow or not slow.next:
            return True

        while fast and fast.next:
            # Находим середину через быстрый и медленный указатели.
            slow = slow.next
            fast = fast.next.next

        prev = None
        cur = slow.next if fast else slow

        while cur:
            # Разворачиваем вторую половину
            next_node = cur.next
            cur.next = prev
            prev = cur
            cur = next_node

        h = head
        h2 = prev

        while h2:
            if h.val != h2.val:
                return False
            h = h.next
            h2 = h2.next
        return True


    def removeElements(self, head: ListNode | None, val: int) -> ListNode | None:
        """
        Удаляет узел по значению
        """
        d_head = ListNode()
        d_head.next = head
        prev = d_head
        while prev.next:
            if prev.next.val == val:
                prev.next = prev.next.next
            else:
                prev = prev.next
        return d_head.next


class MyLinkedList:
    def __init__(self):
        self.dummy = ListNode()  # фиктивная голова, упрощает вставку/удаление
        self.tail = None  # указатель на последний реальный узел
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        cur = self.dummy.next
        for _ in range(index):
            cur = cur.next
        return cur.val

    def add_at_head(self, val: int) -> None:
        new_node = ListNode(val, self.dummy.next)
        self.dummy.next = new_node
        if self.size == 0:
            self.tail = new_node  # если список был пуст, новый узел — и голова, и хвост
        self.size += 1

    def add_at_tail(self, val: int) -> None:
        new_node = ListNode(val)
        if self.size == 0:
            # если список пуст, вставляем в голову и tail
            self.dummy.next = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def add_at_index(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return
        if index == 0:
            self.add_at_head(val)
            return
        if index == self.size:
            self.add_at_tail(val)
            return

        prev = self.dummy
        for _ in range(index):
            prev = prev.next
        new_node = ListNode(val, prev.next)
        prev.next = new_node
        self.size += 1

    def delete_at_index(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        prev = self.dummy
        for _ in range(index):
            prev = prev.next

        if index == self.size - 1:  # удаляем хвост
            self.tail = None if self.size == 1 else prev

        prev.next = prev.next.next
        self.size -= 1
