# Load relevant libraries
import pandas as pd

# Define Functions


def import_stock(symbol, metric):
    """ Read in stock CSV based on data stored in Stock_Data/<symbol>"""

    df = pd.read_csv("Stock_Data/{}.csv".format(symbol),
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

    return df1


def test_run():
    """Run whatever garbage I work on"""

    start_date = '2010-01-22'
    end_date = '2010-01-26'
    symbols = ['IBM', 'SPY', 'GOOG']
    metric = 'Adj Close'

    df_final = import_stock_range(start_date, end_date, metric, symbols)
    print(df_final.head(5))

    """
    dates = pd.date_range(start_date, end_date)
    print(dates)
    df1 = pd.DataFrame(index=dates)
    print(df1)
    dfspy = pd.read_csv("Stock_data/SPY.csv", index_col="Date",
                        parse_dates=True, usecols=['Date', 'Adj Close'],
                        na_values=['nan'])
    df1 = df1.join(dfspy, how='inner')
    print(df1)
    df1 = df1.dropna()
    print(df1)
    """





if __name__ == "__main__":
    test_run()