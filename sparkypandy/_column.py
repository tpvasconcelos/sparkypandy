from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pandas as pd
from py4j.java_gateway import JavaObject
from pyspark.sql import Column, DataFrame

if TYPE_CHECKING:
    from sparkypandy import DataFramy


class Columny(Column):  # type: ignore
    def __init__(self, jc: JavaObject, df_sparky: DataFrame):
        super().__init__(jc=jc)
        self.df_sparky = df_sparky

    @property
    def _name(self) -> str:
        return cast(str, self._jc.toString())

    @classmethod
    def from_spark(cls, col: Column, df_sparky: DataFramy) -> Columny:
        # noinspection PyProtectedMember
        return cls(jc=col._jc, df_sparky=df_sparky)

    def to_pandas(self) -> pd.Series:
        # noinspection PyTypeChecker
        df: pd.DataFrame = self.df_sparky.select(self._name).toPandas()
        return df[self._name]

    # def mean(self) -> float:
    #     r = df_spark.select(F.mean("a").alias("result")).collect()[0].result
