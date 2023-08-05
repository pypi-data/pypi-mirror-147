"""
Command definition for 'export'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Export a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.argument("file", type=click.File("w", encoding="utf-8"))
@click.help_option("-h", "--help")
@click.pass_obj
def export(book, name, file):
    """
    Copy NOTE's contents to FILE.
    """

    note = tools.jobs.disambiguate(book, name)
    tools.jobs.write_file(note, file)
