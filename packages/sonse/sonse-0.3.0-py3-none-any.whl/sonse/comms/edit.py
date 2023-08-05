"""
Command definition for 'edit'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Edit a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def edit(book, name):
    """
    Edit NOTE in your default text editor.
    """

    note = tools.jobs.disambiguate(book, name)
    if text := tools.jobs.edit(note):
        note.write(text)
