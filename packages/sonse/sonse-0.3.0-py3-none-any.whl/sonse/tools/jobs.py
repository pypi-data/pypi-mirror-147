"""
High-level command support functions.
"""

import code
import sys

import click

from sonse import VERSION_STRING


def disambiguate(book, name):
    """
    Return a disambiguated Note from a prefix name, or raise a Click error to
    report the ambiguous name.
    """

    notes = [note for note in book if note.match(name)]

    if len(notes) == 0:
        raise click.ClickException(f"no notes matching {name!r}.")

    elif len(notes) == 1:
        return notes[0]

    else:
        opts = ", ".join(repr(note.name) for note in notes)
        raise click.ClickException(f"ambiguous name, did you mean: {opts}?")


def edit(note):
    """
    Open a Note in the default editor and return the edited text. If this
    function is called during a pytest, return a test value instead.
    """

    if "pytest" in sys.modules:
        return f"Edited {note.name!r}."

    else:
        return click.edit(note.read(), require_save=True)
