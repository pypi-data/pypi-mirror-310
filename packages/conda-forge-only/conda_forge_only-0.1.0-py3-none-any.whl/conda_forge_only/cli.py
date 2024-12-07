"""Command line interface."""

import sys

import click

from conda_forge_only.check import check_files


@click.command()
@click.argument("files", nargs=-1)
def cli(files):
    """Check if conda environment files use conda-forge only."""
    checks_passed = check_files(files)
    sys.exit(0 if all(checks_passed) else 1)
