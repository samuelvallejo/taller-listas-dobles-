from stop import Stop


class BusRoute:
    """Doubly linked list that represents an ordered bus route. O(n)."""

    def __init__(self):
        """Create an empty route with head, tail and current as None. O(1)."""
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def is_empty(self):
        """Return True when the route has no stops. O(1)."""
        return self.size == 0

    def _find(self, name):
        """Walk from head with an auxiliary pointer and return the stop or None. O(n)."""
        pointer = self.head
        while pointer is not None:
            if pointer.name == name:
                return pointer
            pointer = pointer.next
        return None

    def _is_valid_new_name(self, name):
        """Reject empty names and duplicated names before inserting. O(n)."""
        if name == "":
            return False
        if self._find(name) is not None:
            return False
        return True

    def _node_at(self, index):
        """Walk from head with a counter and return the stop at that position. O(n)."""
        position = 1
        pointer = self.head
        while pointer is not None:
            if position == index:
                return pointer
            position = position + 1
            pointer = pointer.next
        return None

    def _insert_after(self, target, name):
        """Link a new stop right after the given pointer and grow the size. O(1)."""
        stop = Stop(name)
        # Four links: new -> target.next, new <- target, target.next.prev -> new, target.next -> new.
        stop.prev = target
        stop.next = target.next
        if target.next is not None:
            target.next.prev = stop
        else:
            self.tail = stop
        target.next = stop
        self.size = self.size + 1
        return True

    def add_first(self, name):
        """Insert a stop at the head of the route. O(n)."""
        if not self._is_valid_new_name(name):
            return False
        stop = Stop(name)
        # New node points forward to the old head, old head points back to it.
        stop.next = self.head
        if self.head is not None:
            self.head.prev = stop
        else:
            self.tail = stop
        self.head = stop
        if self.current is None:
            self.current = stop
        self.size = self.size + 1
        return True

    def add_last(self, name):
        """Insert a stop at the tail of the route in O(1)."""
        if not self._is_valid_new_name(name):
            return False
        stop = Stop(name)
        # New node points back to the old tail, old tail points forward to it.
        stop.prev = self.tail
        if self.tail is not None:
            self.tail.next = stop
        else:
            self.head = stop
        self.tail = stop
        if self.current is None:
            self.current = stop
        self.size = self.size + 1
        return True

    def add_after(self, target_name, new_name):
        """Insert a new stop right after the target stop. O(n)."""
        if not self._is_valid_new_name(new_name):
            return False
        target = self._find(target_name)
        if target is None:
            return False
        return self._insert_after(target, new_name)

    def add_before(self, target_name, new_name):
        """Insert a new stop right before the target stop. O(n)."""
        if not self._is_valid_new_name(new_name):
            return False
        target = self._find(target_name)
        if target is None:
            return False
        stop = Stop(new_name)
        # Four links: new <- target.prev, new -> target, target.prev.next -> new, target.prev -> new.
        stop.next = target
        stop.prev = target.prev
        if target.prev is not None:
            target.prev.next = stop
        else:
            self.head = stop
        target.prev = stop
        self.size = self.size + 1
        return True

    def add_at(self, position, name):
        """Insert a new stop at a 1-based position keeping every link valid. O(n)."""
        if position < 1 or position > self.size + 1:
            return False
        if position == 1:
            return self.add_first(name)
        if position > self.size:
            return self.add_last(name)
        if not self._is_valid_new_name(name):
            return False
        target = self._node_at(position - 1)
        if target is None:
            return False
        return self._insert_after(target, name)

    def remove(self, name):
        """Remove a stop, reconnect its neighbors and fix current. O(n)."""
        stop = self._find(name)
        if stop is None:
            return False
        before = stop.prev
        after = stop.next
        # Bypass the node: the neighbors skip it in both directions.
        if before is not None:
            before.next = after
        else:
            self.head = after
        if after is not None:
            after.prev = before
        else:
            self.tail = before
        if stop is self.current:
            if after is not None:
                self.current = after
            else:
                self.current = before
        self.size = self.size - 1
        return True

    def search(self, name):
        """Return the pointer to the stop with that name, or None. O(n)."""
        return self._find(name)

    def move_next(self):
        """Move the bus to the next stop. O(1)."""
        if self.current is None or self.current.next is None:
            return False
        self.current = self.current.next
        return True

    def move_prev(self):
        """Move the bus to the previous stop. O(1)."""
        if self.current is None or self.current.prev is None:
            return False
        self.current = self.current.prev
        return True

    def go_to(self, name):
        """Place the bus on the given stop. O(n)."""
        stop = self._find(name)
        if stop is None:
            return False
        self.current = stop
        return True

    def go_to_head(self):
        """Place the bus on the first stop. O(1)."""
        self.current = self.head
        return self.current is not None

    def go_to_tail(self):
        """Place the bus on the last stop. O(1)."""
        self.current = self.tail
        return self.current is not None

    def forward_text(self):
        """Build the forward trip string walking from head to tail. O(n)."""
        if self.head is None:
            return "route is empty"
        text = ""
        pointer = self.head
        while pointer is not None:
            text = text + pointer.name
            if pointer.next is not None:
                text = text + " -> "
            pointer = pointer.next
        return text

    def backward_text(self):
        """Build the backward trip string walking from tail to head. O(n)."""
        if self.tail is None:
            return "route is empty"
        text = ""
        pointer = self.tail
        while pointer is not None:
            text = text + pointer.name
            if pointer.prev is not None:
                text = text + " -> "
            pointer = pointer.prev
        return text

    def neighbors_text(self, name):
        """Describe the previous and the next stop of a given stop. O(n)."""
        stop = self._find(name)
        if stop is None:
            return "stop not found"
        if stop.prev is None:
            previous = "none"
        else:
            previous = stop.prev.name
        if stop.next is None:
            following = "none"
        else:
            following = stop.next.name
        return "Previous: " + previous + " | Next: " + following
