"""
Command definition for 'copy'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Copy a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.argument("dest", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def copy(book, name, dest):
    """
    Copy NOTE to DEST.
    """

    note = tools.jobs.disambiguate(book, name)
    if dest in book:
        raise click.ClickException(f"{name!r} already exists.")
    else:
        note.copy(dest)
