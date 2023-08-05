"""Console script for qsavvy."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("qsavvy")
    click.echo("=" * len("qsavvy"))
    click.echo("savvy's Quantum Stuff")


if __name__ == "__main__":
    main()  # pragma: no cover
