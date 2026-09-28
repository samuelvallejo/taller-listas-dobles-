class Stop:
    """A single bus stop node with prev and next pointers. O(1)."""

    def __init__(self, name):
        """Create a stop with its name and both pointers set to None. O(1)."""
        self.name = name
        self.prev = None
        self.next = None
