"""
Class definition for 'Base'.
"""

from sonse import tools


class Base:
    """
    A base class for Sonse item classes.
    """

    __slots__ = tuple()

    def __eq__(self, item):
        """
        Return True if the item is equal to another item.
        """

        return isinstance(item, self.__class__) and all(
            [
                getattr(self, slot) == getattr(item, slot, None)
                for slot in self.__class__.__slots__
            ]
        )

    def __hash__(self):
        """
        Return the item's unique hash string.
        """

        return hash(
            (self.__class__.__name__,)
            + tuple(getattr(self, slot) for slot in self.__slots__)
        )

    def __repr__(self):
        """
        Return the item as a code-representative string.
        """

        slots = (repr(getattr(self, slot)) for slot in self.__class__.__slots__)
        return f"{self.__class__.__name__}({', '.join(slots)})"
