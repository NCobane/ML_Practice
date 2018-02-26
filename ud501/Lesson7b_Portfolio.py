import pandas as pd
import os as os
import math as math
import matplotlib.pyplot as mpl
import numpy as np
import time


# Define functions
def symbol_to_path(symbol, base_dir='Stock_Data'):
    """Return CSV file path given ticker symbol"""

    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def import_stock(symbol, metric):
    """ Read in stock CSV based on data stored in Stock_Data/<symbol>"""

    df = pd.read_csv(symbol_to_path(symbol),
                     index_col='Date', parse_dates=True,
                     usecols=['Date', metric], na_values=['nan'])
    # Rename 'Metric' column to ticker symbol to prevent clash
    df_renamed = df.rename(columns={metric: symbol})

    return df_renamed


def import_stock_range(start_date, end_date, metric, symbols):
    """Imports stock data for date range between start_date and end_date
        Note: Stock data located in Stock_data/<symbol>"""

    # Create date range
    dates = pd.date_range(start_date, end_date)

    # Create empty start dataframe with date index
    df1 = pd.DataFrame(index=dates)

    # Join each relevant symbol's stock data
    for sym in symbols:
        df1 = df1.join(import_stock(sym, metric))

    return df1.dropna(how='all')


def normalize_data(df):
    """ Normalize inputted dataframe """
    return df / df.ix[0, :]


def daily_returns(df):
    """Compute and return daily returns for a dataframe of daily stock data"""

    d_returns = (df / df.shift(1)) - 1
    d_returns.ix[0] = 0

    return d_returns


def portfolio_value(stocks, alloc, base):
    """Calculates portfolio value based on allocation of base dollars to stocks"""

    # Calculate % return
    stock_alloc = alloc * stocks
    portfolio_cumulative = stock_alloc.sum(axis=1)

    # Portfolio Value
    p_value = portfolio_cumulative * base

    return p_value


def sharpe_ratio(daily_rets, daily_rf=0):

    # k constant for 252 measurements / yr (daily frequency)
    k = math.sqrt(252)
    print(daily_rets.mean())
    # Annualized Sharpe Ratio
    sr = k * ((daily_rets.mean() - daily_rf.mean()) / daily_rets.std())

    return sr.ix[0]


def test_run():

    # Set initial parameters
    symbols = ['GOOG', 'SPY', 'XOM', 'GLD', 'IBM']
    metric = 'Adj Close'
    start_date = '2009-01-01'
    end_date = '2017-12-31'
    alloc = [0, 1, 0, 0, 0]
    base = 1000000

    # Import stocks
    stock_corpus = import_stock_range(start_date, end_date, metric, symbols)

    # Normalize
    stock_norm = normalize_data(stock_corpus)
    stock_norm2 = stock_norm[1:]

    # Calculate portfolio value
    tot_value = portfolio_value(stock_norm, alloc, base)
    #  print(tot_value.head(50))

    # Set risk-free return rate
    ref_rate = 0.0245
    daily_rate = ((1 + ref_rate) ** (1.0 / 252)) - 1
    ret_r = pd.DataFrame(np.repeat(daily_rate, len(daily_returns(tot_value).index)))
    ret_rf = ret_r + daily_rate



    # Portfolio Stats

    cm_return = tot_value.ix[tot_value.last_valid_index()] - tot_value.ix[tot_value.first_valid_index()]
    cm_pct_return = (cm_return / base) * 100
    avg_daily_ret = daily_returns(tot_value).mean()
    risk = daily_returns(tot_value).std()
    sr = sharpe_ratio(daily_returns(tot_value), ret_rf)

    print('Cumulative Return: ${} ({}%)'.format(cm_return, cm_pct_return))
    print('Avg Daily Return: {}'.format(avg_daily_ret))
    print('Risk (Std Dev of daily returns): {}'.format(risk))
    print('Sharpe Ratio: {}'.format(sr))


if __name__ == "__main__":
    test_run()