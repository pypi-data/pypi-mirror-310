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
