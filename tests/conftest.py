import logging
import os
from datetime import date, datetime

import pandas as pd
import pytest
from pyspark.sql import DataFrame, SparkSession

from sparkypandy import DataFramy


@pytest.fixture(scope="session")  # type: ignore
def spark_session() -> SparkSession:
    print("Setting up a test Spark Session...")
    master = os.getenv("SPARK_MASTER", "local[2]")
    spark_session = SparkSession.builder.master(master).appName("sparky-pandy-local-testing").getOrCreate()
    logger = logging.getLogger("py4j")
    logger.setLevel(logging.WARNING)
    yield spark_session
    print("Tearing down the test Spark Session...")
    spark_session.stop()
    # To avoid Akka rebinding to the same port, since it doesn't unbind
    # immediately on shutdown
    # noinspection PyUnresolvedReferences,PyProtectedMember
    spark_session._jvm.System.clearProperty("spark.driver.port")


@pytest.fixture  # type: ignore
def df_pandas() -> pd.DataFrame:
    df_pandas = pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [2.0, 3.0, 4.0],
            "c": ["string1", "string2", "string3"],
            "d": [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
            "e": [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)],
        }
    )
    return df_pandas


@pytest.fixture  # type: ignore
def df_spark(spark_session: SparkSession, df_pandas: pd.DataFrame) -> DataFrame:
    df_spark = spark_session.createDataFrame(df_pandas)
    return df_spark


@pytest.fixture  # type: ignore
def df_sparky(spark_session: SparkSession, df_pandas: pd.DataFrame) -> DataFramy:
    # noinspection PyProtectedMember
    return DataFramy.from_pandas(spark_session=spark_session, df_pandas=df_pandas)


COLUMN_NAMES = ["a", "b", "c", "d", "e"]
