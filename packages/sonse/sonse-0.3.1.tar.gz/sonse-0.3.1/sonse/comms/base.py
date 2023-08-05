"""
Click base group and type definitions.
"""

import os

import click

from sonse import tools
from sonse import VERSION_STRING
from sonse.items import Book


@click.group(name="sonse", no_args_is_help=True)
@click.help_option("-h", "--help")
@click.version_option("", "-v", "--version", message=VERSION_STRING)
@click.pass_context
def group(ctx):
    """
    Stephen's Obsessive Note-Storage Engine.

    See github.com/rattlerake/sonse for help and bugs.
    """

    ctx.obj = ctx.obj or tools.jobs.init()


class Name(click.ParamType):
    """
    A Custom Click type for name strings.
    """

    name = "name"

    def convert(self, value, param, ctx):
        """
        Convert a user value to a name string.
        """

        return tools.vals.name(str(value))
