import click

from modely.commands.init_config import init_config

cli = click.CommandCollection(sources=[init_config])


def main() -> None:
    cli()
