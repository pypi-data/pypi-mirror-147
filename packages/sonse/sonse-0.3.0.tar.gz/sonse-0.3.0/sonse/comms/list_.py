"""
Command definition for 'list'.
"""

import click

from sonse.comms.base import group, Name

SORTS = {
    "name": lambda note: note.name,
    "size": lambda note: len(note),
}
CHOICE = click.Choice(sorted(SORTS.keys()))


@group.command(name="list", short_help="List all notes.")
@click.argument("text", default="", type=Name())
@click.option("-r", "--reverse", help="Reverse sorting order.", is_flag=True)
@click.option("-s", "--sort", help="Sort by name or size.", default="name", type=CHOICE)
@click.help_option("-h", "--help")
@click.pass_obj
def list_(book, text, sort, reverse):
    """
    List all notes, or notes starting with TEXT.
    """

    notes = book.match(text)

    for note in sorted(notes, key=SORTS[sort], reverse=reverse):
        click.echo(note.name)
