import pandas as pd
import pytest
from pyspark.sql import DataFrame, SparkSession

from sparkypandy import Columny, DataFramy
from sparkypandy.testing import assert_frame_equal, assert_series_equal
from tests.conftest import COLUMN_NAMES


class TestDataFramy:
    def test_to_pandas(self, df_pandas: pd.DataFrame, df_sparky: DataFramy) -> None:
        assert_frame_equal(df_pandas, df_sparky.to_pandas())

    def test_from_spark(self, df_spark: DataFrame, df_sparky: DataFramy) -> None:
        df_sparky_from_spark = DataFramy.from_spark(df_spark=df_spark)
        assert isinstance(df_sparky_from_spark, DataFramy)
        assert_frame_equal(df_sparky.to_pandas(), df_sparky_from_spark.to_pandas())

    def test_from_pandas(self, spark_session: SparkSession, df_pandas: pd.DataFrame) -> None:
        df_sparky_from_pandas = DataFramy.from_pandas(spark_session=spark_session, df_pandas=df_pandas)
        assert isinstance(df_sparky_from_pandas, DataFramy)
        assert_frame_equal(df_pandas, df_sparky_from_pandas.to_pandas())

    # ==================================================================
    # tests: DataFramy.__getitem__
    # ==================================================================

    def test_getitem_raises_for_nonstring_arg(self, df_sparky: DataFramy) -> None:
        with pytest.raises(TypeError):
            _ = df_sparky[["I", "am", "not", "a", "string"]]  # type: ignore

    @pytest.mark.parametrize("col_name", COLUMN_NAMES)  # type: ignore
    def test_getitem_returns_columny(self, df_sparky: DataFramy, col_name: str) -> None:
        assert isinstance(df_sparky[col_name], Columny)

    @pytest.mark.parametrize("col_name", COLUMN_NAMES)  # type: ignore
    def test_getitem_equal_pandas(self, df_pandas: pd.DataFrame, df_sparky: DataFramy, col_name: str) -> None:
        assert_series_equal(df_pandas[col_name], df_sparky[col_name].to_pandas())
