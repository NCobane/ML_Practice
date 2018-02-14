# Load relevant libraries
import pandas as pd
import os as os
import matplotlib.pyplot as mpl

# Define Functions


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


def normalize_data(df):
    """ Normalize inputted dataframe """
    return df / df.ix[0, :]


def test_run():
    """Run whatever garbage I work on"""

    start_date = '2010-01-01'
    end_date = '2010-12-31'
    symbols = ['IBM', 'SPY', 'GOOG']
    metric = 'Adj Close'

    df_final = import_stock_range(start_date, end_date, metric, symbols)

    #print(df_final.ix['2010-01-01':'2010-01-31', ['SPY', 'IBM']])
    # print(df_final[['IBM', 'GOOG']])

    # Plotting
    # plot_data(df_final, "Stock Prices")

    # Normalize price data
    df_norm = normalize_data(df_final)
    print(df_final.head(5))
    print(df_norm.head(10))
    df_norm.plot()
    mpl.show()

    print('Finished!')



if __name__ == "__main__":
    test_run()