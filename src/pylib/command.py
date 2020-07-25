"""Utilities for working with pipes."""
import pandas as pd


def add_command(cxn, command_id, command):
    """Add a pipe to the database."""
    sql = """
        insert or replace into commands
            (command_id, command, order_, pipe_id)
            values (?, ?, ?, ?);
        """
    cxn.execute(sql, (command_id, command, 0, ''))


def select_cmds(cxn):
    """Get pipes as a dataframe."""
    sql = """
        select *
          from commands
      order by pipe_id, order_, command_id, command;"""
    return pd.read_sql(sql, cxn)
