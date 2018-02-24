import pandas as pd
import os as os
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


def portfolio_value(stocks, alloc, base):
    """Calculates portfolio value based on allocation of base dollars to stocks"""

    # Calculate % return
    stock_alloc = alloc * stocks
    portfolio_cumulative = stock_alloc.sum(axis=1)

    # Portfolio Value
    p_value = portfolio_cumulative * base

    return p_value


def sharpe_ratio(portfolio_returns, risk_free):
    pass


def test_run():

    # Set initial parameters
    symbols = ['GOOG', 'SPY', 'XOM', 'GLD', 'IBM']
    metric = 'Adj Close'
    start_date = '2009-01-01'
    end_date = '2017-12-31'
    alloc = [0.2, 0.4, 0.05, 0.15, 0.2]
    base = 1000000

    # Import stocks
    stock_corpus = import_stock_range(start_date, end_date, metric, symbols)

    # Normalize
    stock_norm = normalize_data(stock_corpus)
    stock_norm2 = stock_norm[1:]

    # Calculate portfolio value
    tot_value = portfolio_value(stock_norm, alloc, base)
    print(tot_value.tail(50))

    # Cumulative Sharpe Ratio




if __name__ == "__main__":
    test_run()