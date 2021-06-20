import pandas as pd


def sort_series(s: pd.Series) -> pd.Series:
    """Sorts rows of a pandas Series."""
    return s.sort_values().reset_index(drop=True)


def sort_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Sorts columns and rows of a pandas DataFrame."""
    # sort columns
    columns = sorted(df.columns)
    df = df[columns]
    # sort rows
    df = df.sort_values(columns).reset_index(drop=True)
    return df


def assert_series_equal(s1: pd.Series, s2: pd.Series) -> None:
    pd.testing.assert_series_equal(
        sort_series(s1),
        sort_series(s2),
    )


def assert_frame_equal(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    pd.testing.assert_frame_equal(
        sort_dataframe(df1),
        sort_dataframe(df2),
    )
