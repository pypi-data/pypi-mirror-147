#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This CLI tool can be used to interact with Assetnote Continuous Security's GraphQL API

.. note::

    todo: add note about viewing documentation

.. currentmodule:: assetnote_cli.cli
.. moduleauthor:: shubham_shah <sshah@assetnote.io>
"""

import logging
import click
from .__init__ import __version__
from .__init__ import Info, pass_info

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.option(
    "--apikey", "-k", required=True, help="API key for your Assetnote CS instance."
)
@click.option(
    "--instance", "-i", required=True, help="Your Assetnote instance name (i.e demos1)."
)
@pass_info
def cli(info: Info, verbose: int, apikey: str, instance: str):
    """Run assetnote_cli."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose
    info.apikey = apikey
    info.instance = instance


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))
