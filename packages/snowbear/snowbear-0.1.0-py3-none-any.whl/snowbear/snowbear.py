from contextlib import contextmanager
from typing import Any

import pandas as pd
from pandas import DataFrame
from pandas.core.generic import bool_t
from pypika import Dialects
from pypika.queries import QueryBuilder, Query
from sqlalchemy.engine import Engine
from pypika.dialects import SnowflakeQuery


class SnowflakeQueryBuilder(QueryBuilder):
    QUOTE_CHAR = None
    ALIAS_QUOTE_CHAR = '"'
    QUERY_ALIAS_QUOTE_CHAR = ''
    QUERY_CLS = SnowflakeQuery

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(dialect=Dialects.SNOWFLAKE, **kwargs)

    def to_df(self, engine: Engine):
        query = self.__str__()
        return read_sql_query(query, engine=engine)


class Dataset(Query):
    @classmethod
    def _builder(cls, **kwargs: Any) -> "SnowflakeQueryBuilder":
        return SnowflakeQueryBuilder(**kwargs)


def read_sql_query(sql: str, engine: Engine) -> pd.DataFrame:
    if engine.dialect == "snowflake":
        with engine.connect() as connection:
            cursor = connection.connection.cursor()
            df = cursor.execute(sql)
            return df
    else:
        return pd.read_sql_query(sql=sql, con=engine)


def to_sql(
        df,
        name: str,
        con,
        schema=None,
        if_exists: str = "fail",
        index: bool_t = True,
        index_label=None,
        chunksize=None,
        dtype=None,
        method=None,
) -> None:
    if con.dialect == "snowflake":
        return df.to_sql(
            name,
            con=con,
            schema=schema,
            if_exists=if_exists,
            index=index,
            index_label=index_label,
            chunksize=chunksize,
            dtype=dtype,
            method=sno,
        )
    else:
        return df.to_sql(
            name,
            con=con,
            schema=schema,
            if_exists=if_exists,
            index=index,
            index_label=index_label,
            chunksize=chunksize,
            dtype=dtype,
            method=method,
        )


@contextmanager
def with_dataset(sql: str, engine) -> pd.DataFrame:
    if engine.dialect == "snowflake":
        with engine.connect() as connection:
            cursor = connection.connection.cursor()
            df = cursor.execute(sql)
            return df
    else:
        return pd.read_sql_query(sql=sql, con=engine)
