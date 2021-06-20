import pandas as pd
import pytest

from sparkypandy.testing import assert_frame_equal, assert_series_equal, sort_dataframe, sort_series

s = pd.Series([4, 3, 1, 2, 5])
s_sorted = pd.Series([1, 2, 3, 4, 5])


df = pd.DataFrame({"B": [10, 7, 8, 9, 6], "A": [5, 2, 3, 4, 1]})
df_sorted = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [6, 7, 8, 9, 10]})


def test_sort_series() -> None:
    pd.testing.assert_series_equal(s_sorted, sort_series(s))


def test_sort_dataframe() -> None:
    pd.testing.assert_frame_equal(df_sorted, sort_dataframe(df))


def test_assert_series_equal() -> None:
    assert_series_equal(s, s)
    assert_series_equal(s, s_sorted)
    with pytest.raises(AssertionError):
        pd.testing.assert_series_equal(s, s_sorted)


def test_assert_frame_equal() -> None:
    assert_frame_equal(df, df)
    assert_frame_equal(df, df_sorted)
    with pytest.raises(AssertionError):
        pd.testing.assert_frame_equal(df, df_sorted)
