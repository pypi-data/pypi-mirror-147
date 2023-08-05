"""
Command definition for 'create'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Create a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.option("-e", "--edit", help="Edit note after creation.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def create(book, name, edit):
    """
    Create NOTE if it does not exist.
    """

    if name in book:
        raise click.ClickException(f"{name!r} already exists.")

    else:
        note = book.create(name)
        if edit:
            tools.jobs.edit(note)
