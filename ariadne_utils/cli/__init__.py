import typing

import click
from .utils import generate_new_schema


@click.group()
def cli():
    """
    Command line tools for ariadne utils
    """
    pass


@cli.command()
def new_schema():
    """
    Generate new graphql schema and place in current directory
    """
    generate_new_schema()
