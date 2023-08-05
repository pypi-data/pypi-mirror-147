"""
Command definition for 'delete'.
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Delete a note.")
@click.argument("name", metavar="NOTE", type=Name())
@click.option("-f", "--force", help="Bypass confirmation prompt.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def delete(book, name, force):
    """
    Delete NOTE if it exists.
    """

    note = tools.jobs.disambiguate(book, name)
    if force or click.confirm(f"Are you sure you want to delete {name!r}?"):
        note.delete()
    else:
        click.echo("Delete cancelled.")
