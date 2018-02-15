# Import relevant libraries

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
    df_renamed = df.rename(columns={metric:symbol})

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


def plot_data(df, title="Stock prices"):
    """Plot stock prices"""

    ax = df.plot(title=title, fontsize=8)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    mpl.show()


def bollinger_bands(df, window):
    """Takes in a vector dataframe and returns +- 2 stddev data for plotting Bollinger bands"""

    std_rolling = df.rolling(window=window, center=False).std()
    top_band = df.rolling(window=window, center=False).mean() + (2*std_rolling)
    bottom_band = df.rolling(window=window, center=False).mean() - (2*std_rolling)

    return pd.concat([top_band, bottom_band], axis=1)


def daily_returns(df):
    """Compute and return daily returns for a dataframe of daily stock data"""

    d_returns = (df / df.shift(1)) - 1
    d_returns.ix[0, :] = 0

    return d_returns


def test_run():

    # Set up data
    start_date = '2017-01-01'
    end_date = '2017-12-31'
    metric = 'Adj Close'
    stocks = ['SPY', 'GOOG', 'GLD']

    # Grab stock data
    df = import_stock_range(start_date, end_date, metric, stocks)

    # Plot SPY data
    ax = df['SPY'].plot(title='SPY Rolling Mean and Bands', label='SPY')

    # Calculate and plot rolling mean
    rm_SPY = df['SPY'].rolling(window=20, center=False).mean()
    rm_SPY.plot(label='Rolling Mean', ax=ax)

    # Calculate and plot Bollinger bands
    bb_SPY = bollinger_bands(df['SPY'], 20)
    bb_SPY.plot(label='Bollinger Bands', ax=ax)

    # Format plot and show plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    mpl.show()

    # Daily Returns



if __name__ == "__main__":
    test_run()


