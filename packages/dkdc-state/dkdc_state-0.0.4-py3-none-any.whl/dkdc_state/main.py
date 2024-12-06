"""
State base class.
"""

import os
import ibis
import ibis.expr.datatypes as dt  # noqa: F401


class State:
    # initialization
    def __init__(self, dbpath: str = "data.db"):
        self.dbpath = dbpath

        self.wcon, self.rcon = self._cons()

    # reference implementation -- to be overridden
    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ...

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        # return connections
        return wcon, rcon

    def _clear(self, table_names: str | list[str] = None):
        # if table_names is None, clear all tables
        table_names = self.wcon.list_tables() if table_names is None else table_names

        # if table_names is a string, convert to a list
        if isinstance(table_names, str):
            table_names = [table_names]

        # drop views and tables
        for table_name in table_names:
            self.rcon.drop_view(table_name)
            self.wcon.drop_table(table_name)

        # reset connections (recreate tables)
        self.wcon, self.rcon = self._cons()
