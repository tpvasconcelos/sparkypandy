from __future__ import annotations

from typing import TYPE_CHECKING, Union, cast, overload

import pandas as pd
from py4j.java_gateway import JavaObject
from pyspark.sql import Column, functions as F
from typing_extensions import Literal

if TYPE_CHECKING:
    from sparkypandy import DataFramy


class Columny(Column):  # type: ignore
    def __init__(self, jc: JavaObject, df_sparky: DataFramy):
        super().__init__(jc=jc)
        self.df_sparky = df_sparky

    @property
    def _name(self) -> str:
        name = cast(str, self._jc.toString())
        if " AS " in name:
            name = name.split(" AS ")[-1].strip("`")
        return name

    @classmethod
    def from_spark(cls, col: Column, df_sparky: DataFramy) -> Columny:
        # noinspection PyProtectedMember
        return cls(jc=col._jc, df_sparky=df_sparky)

    def to_pandas(self) -> pd.Series:
        # noinspection PyTypeChecker
        df: pd.DataFrame = self.df_sparky.select(self).toPandas()
        return df[self._name]

    # ==================================================================
    # Aggregations
    # ==================================================================

    @overload
    def mean(self, alias: str = None, collect: Literal[False] = False) -> Columny:
        ...

    @overload
    def mean(self, alias: str = None, collect: Literal[True] = True) -> float:
        ...

    def mean(self, alias: str = None, collect: bool = False) -> Union[Columny, float]:
        if not alias:
            alias = f"mean({self._name})"
        col = F.mean(self).alias(alias)
        if collect:
            result: float = self.df_sparky.select(col).collect()[0][alias]
            return result
        return Columny.from_spark(col=col, df_sparky=self.df_sparky)
