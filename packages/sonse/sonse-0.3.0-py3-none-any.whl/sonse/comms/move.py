"""
Command definition for 'move'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Rename a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.argument("dest", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def move(book, name, dest):
    """
    Rename NOTE to DEST.
    """

    note = tools.jobs.disambiguate(book, name)
    if dest in book:
        raise click.ClickException(f"{name!r} already exists.")
    else:
        note.rename(dest)
