import pandas as pd
import pytest
from pyspark.sql import DataFrame

from sparkypandy import Columny, DataFramy
from sparkypandy.testing import assert_series_equal
from tests.conftest import ALL_COLUMN_NAMES, NUMERIC_COLUMN_NAMES


class TestColumny:
    @pytest.mark.parametrize("col_name", ALL_COLUMN_NAMES)  # type: ignore
    def test_under_name(self, df_sparky: DataFramy, col_name: str) -> None:
        assert df_sparky[col_name]._name == col_name

    @pytest.mark.parametrize("col_name", ALL_COLUMN_NAMES)  # type: ignore
    def test_from_spark(self, df_spark: DataFrame, df_sparky: DataFramy, col_name: str) -> None:
        # TODO: Not sure how to test this class method. Also not sure how to
        #       test equality for a Column instance. For now, I am simply
        #       asserting that both instance dicts are equal.
        #       Maybe compare result from `.to_pandas()` here too?
        col_spark = df_spark[col_name]
        actual = Columny.from_spark(col=col_spark, df_sparky=df_sparky).__dict__
        expected = Columny(jc=col_spark._jc, df_sparky=df_sparky).__dict__
        assert actual == expected

    @pytest.mark.parametrize("col_name", ALL_COLUMN_NAMES)  # type: ignore
    def test_to_pandas(self, df_sparky: DataFramy, df_pandas: pd.DataFrame, col_name: str) -> None:
        col_sparky = df_sparky[col_name]
        col_pandas = df_pandas[col_name]
        assert_series_equal(col_sparky.to_pandas(), col_pandas)

    # ==================================================================
    # test aggregations
    # ==================================================================

    # test: mean()

    @pytest.mark.parametrize("col_name", NUMERIC_COLUMN_NAMES)  # type: ignore
    def test_mean(self, df_sparky: DataFramy, df_pandas: pd.DataFrame, col_name: str) -> None:
        mean_df_sparky = df_sparky[col_name].mean().to_pandas()
        mean_pandas = df_pandas[col_name].mean()
        assert mean_df_sparky.iloc[0] == mean_pandas
        pd.testing.assert_series_equal(mean_df_sparky, pd.Series(mean_pandas, name=f"mean({col_name})"))

    @pytest.mark.parametrize("col_name", NUMERIC_COLUMN_NAMES)  # type: ignore
    def test_mean_with_alias(self, df_sparky: DataFramy, df_pandas: pd.DataFrame, col_name: str) -> None:
        target_alias_str = "target_alias_str"
        mean_df_sparky = df_sparky[col_name].mean(alias=target_alias_str).to_pandas()
        mean_pandas = df_pandas[col_name].mean()
        assert mean_df_sparky.iloc[0] == mean_pandas
        pd.testing.assert_series_equal(mean_df_sparky, pd.Series(mean_pandas, name=target_alias_str))

    @pytest.mark.parametrize("col_name", NUMERIC_COLUMN_NAMES)  # type: ignore
    def test_mean_with_collect(self, df_sparky: DataFramy, df_pandas: pd.DataFrame, col_name: str) -> None:
        mean_sparky = df_sparky[col_name].mean(collect=True)
        mean_pandas = df_pandas[col_name].mean()
        assert mean_sparky == mean_pandas
