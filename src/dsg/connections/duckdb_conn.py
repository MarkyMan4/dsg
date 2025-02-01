import duckdb
import polars as pl

from dsg.connections.base import DatabaseConnection


class DuckDBConnection(DatabaseConnection):
    def __init__(self, db_file: str):
        self._db_file = db_file

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(self._db_file)

    def read_sql(self, query: str) -> pl.DataFrame:
        conn = self._connect()
        df = conn.sql(query).pl()
        conn.close()

        return df
