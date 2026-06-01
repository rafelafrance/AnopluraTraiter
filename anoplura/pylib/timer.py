"""Functions for timing event and reporting elapsed time."""

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from anoplura.pylib import log

if TYPE_CHECKING:
    from argparse import Namespace
    from pathlib import Path


def job_began(
    file_name: str | Path | None = None, *, args: Namespace | None
) -> datetime:
    """Report on the time the entire job started."""
    log.started(file_name, args=args)
    return datetime.now()


def job_elapsed(job_began: datetime) -> None:
    """Report on how long the job took."""
    job_elapsed = str(datetime.now() - job_began)
    msg = f"Job elapsed {job_elapsed}"
    logging.info(msg)
    log.finished()


def task_began(name: str) -> datetime:
    if name:
        logging.info(f"{name} started")
    return datetime.now()


def task_elapsed(started: datetime, name: str = "") -> str:
    """Report on how long a generic event took."""
    elapsed_ = str(datetime.now() - started)
    if name:
        msg = f"{name} elapsed {elapsed_}"
        logging.info(msg)
    return elapsed_
