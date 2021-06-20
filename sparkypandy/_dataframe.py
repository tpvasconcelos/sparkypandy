from __future__ import annotations

import pandas as pd
from pyspark.sql import DataFrame, SparkSession

from sparkypandy._column import Columny


class DataFramy(DataFrame):  # type: ignore
    @classmethod
    def from_spark(cls, df_spark: DataFrame) -> DataFramy:
        # noinspection PyProtectedMember
        return cls(jdf=df_spark._jdf, sql_ctx=df_spark.sql_ctx)

    @classmethod
    def from_pandas(cls, spark_session: SparkSession, df_pandas: pd.DataFrame) -> DataFramy:
        df_spark = spark_session.createDataFrame(df_pandas)
        return cls.from_spark(df_spark)

    def to_pandas(self) -> pd.DataFrame:
        """PEP8-compliant alias to toPandas()"""
        # noinspection PyTypeChecker
        return super().toPandas()

    def __getitem__(self, item: str) -> Columny:
        if not isinstance(item, str):
            raise TypeError(f"Expected a string key, not {item}")
        col = super().__getitem__(item=item)
        return Columny.from_spark(col=col, df_sparky=self)
