import urllib.request


def fetch_data(symbol, time_frame='d'):
    # d -> daily, w -> weekly, m -> monthly.

    url = "http://real-chart.finance.yahoo.com/table.csv?s="+symbol+"&a=11&b=22&c=1998&d=04&e=9&f=2018&g="+time_frame+"+&ignore=.csv"

    urllib.request.urlretrieve(url, 'Stock_Data/{}.csv'.format(symbol))
    print("DEBUG: Downloading for "+symbol)
    print("DEBUG: URL:"+url)


def test_run():
    # Choose stock symbols to read
    symbols = ['AAPL', 'XOM']
    for symbol in symbols:
        fetch_data(symbol)  # Download csv for symbol loading.


if __name__ == "__main__":
    test_run()