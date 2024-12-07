"""Entrypoint for Dabapush CLI"""

import sys

import click
from loguru import logger as log

from dabapush.Dabapush import Dabapush

from .create_subcommand import create
from .reader_subcommand import reader
from .run_subcommand import run
from .update_subcommand import update
from .writer_subcommand import writer


@click.group()
@click.option("--logfile", help="file to log in (optional)")
@click.option("--loglevel", default="INFO", help="the level to log, yk")
@click.pass_context
def cli(ctx: click.Context, logfile, loglevel):
    """Dabapush"""
    # prepare log options
    log.remove()

    if logfile is not None:
        if loglevel is None:
            loglevel = "DEBUG"
            log.add(sys.stdout, level=loglevel)
        log.add(logfile, level=loglevel)
    # do standard logging into STDOUT
    else:
        log.add(sys.stdout, level="DEBUG")
    # prepare context
    ctx.ensure_object(Dabapush)

    db: Dabapush = ctx.obj
    log.debug(f"Starting DabaPush in {db.working_dir}.")


cli.add_command(reader)
cli.add_command(writer)
cli.add_command(run)
cli.add_command(create)
cli.add_command(update)
