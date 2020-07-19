"""Utilities for working with pipes."""
import pandas as pd

from .db import connect


def add_pipe(pipe_id, pipe):
    """Add a pipe to the database."""
    sql = """
        INSERT OR REPLACE INTO pipes
            (pipe_id, pipe, order_, parent)
            VALUES (?, ?, ?, ?);
        """
    with connect() as cxn:
        cxn.execute(sql, (pipe_id, pipe, 0, ''))


def select_pipes():
    """Get pipes as a dataframe."""
    sql = """select * from pipes order by parent, order_, pipe_id;"""
    with connect() as cxn:
        return pd.read_sql(sql, cxn)
