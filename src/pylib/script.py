"""Utilities for working with pipes."""
import pandas as pd


def add_script(cxn, script_id, script):
    """Add a pipe to the database."""
    sql = """
        insert or replace into scripts
            (script_id, script, pipe_id, order_)
            values (?, ?, ?, ?);
        """
    cxn.execute(sql, (script_id, script, '', 0))


def select_scripts(cxn):
    """Get pipes as a dataframe."""
    sql = """
        select *
          from scripts
      order by pipe_id, order_, script_id, script;"""
    return pd.read_sql(sql, cxn)
