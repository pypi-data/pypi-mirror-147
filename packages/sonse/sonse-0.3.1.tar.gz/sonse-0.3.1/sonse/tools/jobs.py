"""
High-level command support functions.
"""

import os
import sys

import click

from sonse import tools
from sonse.items import Book

BOOK_DIRE = "$HOME/.config/sonse"
BOOK_PATH = "$HOME/.config/sonse/sonse.zip"


def disambiguate(book, name):
    """
    Return a disambiguated Note from a prefix name, or raise a Click error to
    report the ambiguous name.
    """

    name = tools.vals.name(name)
    notes = [note for note in book if note.match(name)]

    if len(notes) == 1:
        return notes[0]

    elif not notes:
        raise click.ClickException(f"no notes matching {name!r}.")

    else:
        opts = ", ".join(repr(note.name) for note in notes)
        raise click.ClickException(f"ambiguous name, did you mean: {opts}?")


def edit(note):
    """
    Open a Note in the default editor and return the edited text. If this
    function is called during a pytest, return a test value instead.
    """

    if "pytest" in sys.modules:
        note.write(f"Edited {note.name!r}.")

    else:
        if text := click.edit(note.read(), require_save=True):
            note.write(text)


def init():
    """
    Return a new or existing Book in the default location.
    """

    if "HOME" not in os.environ:
        raise click.ClickException("'$HOME' does not exist.")

    dire = tools.path.expand(BOOK_DIRE)
    path = tools.path.expand(BOOK_PATH)

    try:
        if not os.path.isdir(dire):
            os.makedirs(dire)
        if not os.path.isfile(path):
            tools.file.create(path)

    except Exception:
        raise click.ClickException(f"cannot create archive at {path!r}.")

    return Book(path)


def read_file(note, file):
    """
    Write the contents of an external file to a Note.
    """

    try:
        note.write(file.read())

    except Exception:
        raise click.ClickException("cannot read from {file!r}.")


def write_file(note, file):
    """
    Write the contents of a Note to an external file.
    """

    try:
        file.write(note.read())

    except Exception:
        raise click.ClickException("cannot write to {file!r}.")
