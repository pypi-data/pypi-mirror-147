"""
Command definition for 'import'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(name="import", short_help="Import a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.argument("file", type=click.File("r", encoding="utf-8"))
@click.option("-e", "--edit", help="Edit note after import.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def import_(book, name, file, edit):
    """
    Copy FILE's contents to NOTE.
    """

    note = book.get(name, create=True)
    tools.jobs.read_file(note, file)

    if edit:
        tools.jobs.edit(note)
