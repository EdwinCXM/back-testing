# data_feed.py
import pandas as pd
import glob
import os
from datetime import datetime


def load_data(COIN):
    """
    Function will load data for the data found at CryptoDataDownload.com
    """
    folder_name = f'data/{COIN}/'
    li = []
    for filename in os.listdir(folder_name):
        df = pd.read_csv(folder_name + filename, index_col=None)
        df.columns = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]
        li.append(df)
    data = pd.concat(li, axis=0, ignore_index=True)
    # data = pd.read_csv(csv_name)    # use pandas to read file from site
    data.rename({"open_time": "datetime", "open": "Open", "high": "High", "low": "Low", "close": "Close"}, axis=1, inplace=True)
    data.drop(columns=["volume", "close_time", "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"], inplace=True) # drop columns we dont need
    data["datetime"] = pd.to_datetime(data["datetime"], unit="ms")
    data.set_index('datetime', inplace=True)
    data.sort_index(inplace=True)
    print(data)

    return data  # return our large and combined dataframe

