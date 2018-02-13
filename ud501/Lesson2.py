# Import relevant libraries
import pandas as pd
import matplotlib.pyplot as plt

# Define functions

def import_stock(symbol):
    """ Read in stock CSV based on data stored in Stock_Data/<symbol>"""
    df = pd.read_csv("Stock_Data/{}.csv".format(symbol))  # read in data
    return df


def test_run():
    df = pd.read_csv("Stock_Data/HCP.csv")
    print(df.tail(5))  # print last 5 values of dataframe
    print(df[10:20])


def get_max_close(symbol):
    """ Return the maximum closing value for stock indicated by symbol.
    Note: Data for stock stored in data/<symbol>.csv"""

    df = import_stock(symbol)
    return df['Close'].max()  # Compute and return max close


def get_mean_volume(symbol):
    """ Return the mean volume for stock indicated by symbol.
    Note: Data for stock stored in stock_data/<symbol>.csv"""

    df = import_stock(symbol)
    return df['Volume'].mean()  # Compute and return mean volume


if __name__ == "__main__":
    symb = 'HCP'
    df = import_stock(symb)
    print('Max Close: ', symb, get_max_close(symb))
    print('Mean Volume: ', symb, get_mean_volume(symb))

    # Plotting
    df['Adj Close'].plot()
    plt.show()  # must be called to show plots

    df[['Close', 'Adj Close']].plot()
    plt.show()
