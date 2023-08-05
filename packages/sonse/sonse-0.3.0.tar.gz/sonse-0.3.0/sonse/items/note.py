"""
Class definition for 'Note'.
"""

from sonse import tools
from sonse.items.base import Base


class Note(Base):
    """
    A single plaintext note in a Book.
    """

    __slots__ = ("path", "name")

    def __init__(self, path, name):
        """
        Initialise the Note.
        """

        self.path = str(path)
        self.name = tools.vals.name(name)

    def __iter__(self):
        """
        Yield each line in the Note's body.
        """

        yield from self.read().splitlines()

    def __len__(self):
        """
        Return the length of the Note's body.
        """

        return len(self.read())

    def delete(self):
        """
        Delete the Note from its archive.
        """

        tools.file.delete(self.path, self.name + ".txt")

    def match(self, text):
        """
        Return True if the Note's name starts with a string.
        """

        return self.name.startswith(tools.vals.name(text))

    def read(self):
        """
        Return the contents of the Note as a string.
        """

        body = tools.file.read(self.path, self.name + ".txt")
        return tools.vals.body(body)

    def rename(self, name):
        """
        Move the Note to another name in the archive.
        """

        dest = tools.vals.name(name) + ".txt"
        tools.file.rename(self.path, self.name + ".txt", dest)
        self.__init__(self.path, name)

    def write(self, body):
        """
        Overwrite the Note's contents with a string.
        """

        body = tools.vals.body(body)
        tools.file.write(self.path, self.name + ".txt", body)
