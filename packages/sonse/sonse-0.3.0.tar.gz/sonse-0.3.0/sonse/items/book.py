"""
Class definition for 'Book'.
"""

from sonse import tools
from sonse.items.base import Base
from sonse.items.note import Note


class Book(Base):
    """
    A single zipfile archive of Notes.
    """

    __slots__ = ("path",)

    def __init__(self, path):
        """
        Initialise the Book.
        """

        self.path = str(path)

    def __contains__(self, name):
        """
        Return True if the Book contains a named Note.
        """

        return tools.vals.name(name) in self.read().keys()

    def __getitem__(self, name):
        """
        Return a Note from the Book using dict syntax.
        """

        return self.read()[tools.vals.name(name)]

    def __iter__(self):
        """
        Yield all Notes in the Book in alphabetical name order.
        """

        notes = self.read().values()
        yield from sorted(notes, key=lambda note: note.name)

    def __len__(self):
        """
        Return the number of Notes in the Book.
        """

        return len(self.read().keys())

    def create(self, name):
        """
        Create and return a new empty Note in the Book.
        """

        name = tools.vals.name(name)
        tools.file.write(self.path, f"{name}.txt", "")
        return Note(self.path, name)

    def get(self, name, *, create=False):
        """
        Return an existing Note by name. If "create" is True, create the Note
        if it doesn't exist.
        """

        name = tools.vals.name(name)
        notes = self.read()

        if name in notes:
            return notes[name]
        elif create:
            return self.create(name)
        else:
            return None

    def match(self, text):
        """
        Yield all Notes in the Book with names starting with a string.
        """

        yield from (note for note in self if note.match(text))

    def read(self):
        """
        Return a dict of existing Notes in the Book.
        """

        names = map(tools.path.name, tools.file.iterate(self.path, "txt"))
        notes = (Note(self.path, name) for name in names)
        return {note.name: note for note in notes}
