from abc import ABC, abstractmethod

import polars as pl

from dsg.models import ConnectionInfo

CONN_TYPE_DUCKDB = "duckdb"


class DatabaseConnection(ABC):
    @abstractmethod
    def _connect(self):
        # get a "connection" object for the database
        pass

    @abstractmethod
    def read_sql(query: str) -> pl.DataFrame:
        pass


def get_connection(conn_info: ConnectionInfo) -> DatabaseConnection:
    """
    Figure out which DatabaseConnection implementation to use based on the connection
    info in the dsg.yml file

    :param conn_info: connection information from dsg.yml
    :type conn_info: ConnectionInfo
    :return: one of the DatabaseConnection implementations
    :rtype: DatabaseConnection
    """
    if conn_info.type == "duckdb":
        from .duckdb_conn import DuckDBConnection

        return DuckDBConnection(conn_info.settings["file"])
    else:
        raise Exception(f"Unsupported connection type: {conn_info.type}")
