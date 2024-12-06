from pandas import DataFrame


def calculate_sharpe_ratio(df: DataFrame, column_name='close', risk_free_rate=0.04) -> float:
    """
    Calculate the Sharpe ratio of a given DataFrame.
    :param df: DataFrame
    :param column_name: str
    :param risk_free_rate: float
    :param trading_fee_rate: float
    :return: float
    """

    assert column_name in df.columns, f"{column_name} not in df.columns"
    assert risk_free_rate >= 0, "risk_free_rate must be greater than 0"
    assert risk_free_rate <= 1, "risk_free_rate must be less than 1"

    # Calculate the daily returns of the stock
    df['daily_returns'] = df[column_name].pct_change()
    # Calculate the excess returns
    df['excess_returns'] = df['daily_returns'] - risk_free_rate
    # Calculate the mean of the excess returns
    avg_excess_return = df['excess_returns'].mean()
    # Calculate the standard deviation of the excess returns
    std_excess_return = df['excess_returns'].std()
    # Calculate the Sharpe ratio
    sharpe_ratio = avg_excess_return / std_excess_return
    return sharpe_ratio
