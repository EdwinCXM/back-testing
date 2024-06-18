# data_feed.py
import pandas as pd


def load_data(coin, interval):
    """
    Function will load data for the data found at binance klines service, doesn't work in the US
    """
    sym = coin.split("/")[0]    # get the symbol in front of the slash, ie BTC from BTC/USD
    sym_base = coin.split("/")[1]   # get the base symbol, ie USD in BTC/USD
    URL = f"https://api.binance.com/api/v3/klines?symbol={sym}{sym_base}&interval=1{interval}"   # path to file
    data = pd.read_csv(URL, skiprows=1)    # use pandas to read file from site
    data['Date'] = pd.to_datetime(data['Date'])
    data['datetime'] = data['Date'].apply(lambda x: int(x.timestamp() * 1000))
    data["datetime"] = data["datetime"].values.astype(dtype='datetime64[ms]')
    data.sort_values('datetime', ascending=True, inplace=True)  # we need to sort the data to have most recent data last in file
    data.set_index('datetime', inplace=True)
    data.drop(columns=[f'Volume {sym}', f'Volume {sym_base}', 'tradecount', 'Symbol', 'Unix', 'Date'], inplace=True) # drop columns we dont need
    return data  # return our large and combined dataframe