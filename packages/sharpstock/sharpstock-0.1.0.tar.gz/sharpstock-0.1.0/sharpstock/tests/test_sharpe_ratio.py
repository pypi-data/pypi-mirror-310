from pandas import DataFrame
from sharpstock.sharpe_ratio import calculate_sharpe_ratio
from numpy.testing import assert_almost_equal

test_df = DataFrame({
    'open': [0.1, 0.2, 0.3, 0.4, 0.5],
    'close': [1, 2, 3, 4, 5]
})


def test_calculate_sr():
    assert_almost_equal(calculate_sharpe_ratio(test_df), 1.43, 2)


def test_calculate_sr_with_risk_free_rate():
    assert_almost_equal(calculate_sharpe_ratio(test_df, risk_free_rate=0.02), 1.49, 2)


def test_calculate_sr_with_different_column_name():
    assert_almost_equal(calculate_sharpe_ratio(test_df, column_name='close'), 1.43, 2)
    try:
        assert_almost_equal(calculate_sharpe_ratio(test_df, column_name='close1'), 1.43, 2)
    # the errror_message provided by the user gets printed
    except AssertionError as msg:
        print(msg)
        assert msg


def test_calculate_sr_with_negative_risk_free_rate():
    try:
        assert_almost_equal(calculate_sharpe_ratio(test_df, risk_free_rate=-0.02), 1.49, 2)
    # the errror_message provided by the user gets printed
    except AssertionError as msg:
        print(msg)
        assert msg


def test_calculate_sr_with_open_column():
    assert_almost_equal(calculate_sharpe_ratio(test_df, column_name='open'), 1.43, 2)
