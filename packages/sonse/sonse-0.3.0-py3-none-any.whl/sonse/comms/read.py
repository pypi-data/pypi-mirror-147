"""
Command definition for 'read'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Read a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def read(book, name):
    """
    Print NOTE's contents to screen.
    """

    note = tools.jobs.disambiguate(book, name)
    click.echo(note.read())
