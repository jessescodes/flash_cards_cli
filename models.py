# flash_card_cli.models.py

from __future__ import annotations

import time


class FlashCard:
    def __init__(self, front: str, back: str):
        self.id: int | None = None
        self.front = front
        self.back = back
        self.grade: int = 3
        self.EF: float = 2.5
        self.repetition: int = 0
        self.interval = 0
        self.review_timestamp = time.time()

    def calculate_next_interval(self):
        new_ef = self.EF + (0.1 - (5 - self.grade)) * (0.08 + (5 - self.grade))

        if self.grade < 3:
            new_reps = 0
            new_interval = 1
        else:
            new_reps = self.repetition + 1
            if new_reps == 1:
                new_interval = 1
            elif new_reps == 2:
                new_interval = 6
            else:
                new_interval = round(self.interval * new_ef)

        seconds_per_day = 86_400
        next_review_timestamp = time.time() + (new_interval * seconds_per_day)
        self.EF = new_ef
        self.repetition = new_reps
        self.interval = new_interval
        self.review_timestamp = next_review_timestamp
        return self


class FlashNode:
    def __init__(self, flash_card: FlashCard | None = None, timestamp: float = 0.0):
        self.flash_card: FlashCard | None = flash_card if flash_card else None
        self.timestamp = flash_card.review_timestamp if flash_card else timestamp
        self.next: FlashNode | None = None
        self.prev: FlashNode | None = None


class FlashQueue:
    def __init__(self):
        self.head = FlashNode(timestamp=float("-inf"))
        self.tail = FlashNode(timestamp=float("inf"))
        self.head.next = self.tail
        self.tail.prev = self.head
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __contains__(self, card: FlashCard):
        current = self.head.next
        if current == self.tail:
            return False
        assert current is not None
        while current.next is not None and current.next is not self.tail:
            if current.flash_card == card:
                return True
            else:
                current = current.next
        return current.flash_card == card

    def push(self, flash_card: FlashCard):
        new_node = FlashNode(flash_card)
        current = self.head.next
        while (
            current is not None
            and current is not self.tail
            and current.timestamp <= new_node.timestamp
        ):
            current = current.next

        assert current is not None

        new_node.next = current
        new_node.prev = current.prev
        if current.prev:
            current.prev.next = new_node
        current.prev = new_node
        self.length += 1

    def pop(self) -> FlashCard | None:
        if self.head.next is self.tail:
            return None
        target = self.head.next
        assert target is not None
        self.head.next = target.next
        if target.next:
            target.next.prev = self.head
        target.next = None
        target.prev = None
        self.length -= 1

        return target.flash_card
