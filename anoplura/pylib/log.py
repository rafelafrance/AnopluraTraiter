"""Logging setup and lifecycle helpers for CLI scripts."""

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import Namespace


def setup_logger(file_name: str | Path | None = None) -> None:
    """Configure the root logger with optional file output."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if file_name:
        logging.getLogger().addHandler(logging.FileHandler(file_name))


def module_name() -> str:
    """Return the stem of the currently running script."""
    return Path(sys.argv[0]).stem


def started(
    file_name: str | Path | None = None, *, args: Namespace | None = None
) -> None:
    """Initialize logging and record script start with arguments."""
    setup_logger(file_name)
    logging.info("=" * 80)
    msg = f"{module_name()} started"
    logging.info(msg)
    if args:
        log_args(args)


def finished() -> None:
    """Log script completion."""
    msg = f"{module_name()} finished"
    logging.info(msg)


def log_args(args: Namespace) -> None:
    """Log each argument value, excluding sensitive fields like api_key."""
    for key, val in sorted(vars(args).items()):
        if key != "api_key":
            msg = f"Argument: {key} = {val}"
            logging.info(msg)
