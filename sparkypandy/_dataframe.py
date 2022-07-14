from __future__ import annotations

from typing import Union

import pandas as pd
from pyspark.sql import Column, DataFrame, SparkSession

from sparkypandy._column import Columny


class DataFramy(DataFrame):  # type: ignore
    @classmethod
    def from_spark(cls, df_spark: DataFrame) -> DataFramy:
        """Creates a :class:`DataFramy` from an :class:`DataFrame`."""
        # noinspection PyProtectedMember
        return cls(jdf=df_spark._jdf, sql_ctx=df_spark.sql_ctx)

    @classmethod
    def from_pandas(cls, spark_session: SparkSession, df_pandas: pd.DataFrame) -> DataFramy:
        """Creates a :class:`DataFramy` from an :class:`~pd.DataFrame`."""
        df_spark = spark_session.createDataFrame(df_pandas)
        return cls.from_spark(df_spark)

    def to_pandas(self) -> pd.DataFrame:
        """Snake-case (PEP8-compliant) alias to
        :py:meth:`~DataFramy.toPandas()`.
        """
        # noinspection PyTypeChecker
        return super().toPandas()

    def __getitem__(self, item: Union[str, Column, list, tuple, int]) -> Union[Columny, DataFramy]:
        result = super().__getitem__(item=item)
        if isinstance(result, Column):
            return Columny.from_spark(col=result, df_sparky=self)
        elif isinstance(result, DataFrame):
            return DataFramy.from_spark(df_spark=result)
        else:
            raise TypeError(f"Unexpected result type: {type(result)}")
