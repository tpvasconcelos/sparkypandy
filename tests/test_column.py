import pandas as pd
import pytest
from pyspark.sql import DataFrame

from sparkypandy import Columny, DataFramy
from tests.conftest import COLUMN_NAMES


class TestColumny:
    @pytest.mark.parametrize("col_name", COLUMN_NAMES)  # type: ignore
    def test_under_name(self, df_sparky: DataFramy, col_name: str) -> None:
        assert df_sparky[col_name]._name == col_name

    @pytest.mark.parametrize("col_name", COLUMN_NAMES)  # type: ignore
    def test_from_spark(self, df_spark: DataFrame, df_sparky: DataFramy, col_name: str) -> None:
        # TODO: Not sure how to test this class method. Also not sure how to
        #       test equality for a Column instance. For now, I am simply
        #       asserting that both instance dicts are equal.
        col_spark = df_spark[col_name]
        calculated = Columny.from_spark(col=col_spark, df_sparky=df_sparky).__dict__
        expected = Columny(jc=col_spark._jc, df_sparky=df_sparky).__dict__
        assert calculated == expected

    @pytest.mark.parametrize("col_name", COLUMN_NAMES)  # type: ignore
    def test_to_pandas(self, df_sparky: DataFramy, df_pandas: pd.DataFrame, col_name: str) -> None:
        col_sparky = df_sparky[col_name]
        col_pandas = df_pandas[col_name]
        pd.testing.assert_series_equal(col_sparky.to_pandas(), col_pandas)
