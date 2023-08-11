import pandas as pd
import time

from fetcher import CryptoFetcher  
from logger import Log
import filemanager as fm  


FILE_PATH = 'files/'

def retriveSymbols():
    """
    Retrieve symbols from the 'symbols.csv' file.

    Returns:
        pd.DataFrame: DataFrame containing the symbols.
    """
    symbols = pd.read_csv('symbols.csv')
    return symbols

def retrive_from(symbol):
    """
    Retrieve the 'from' timestamp for a symbol.

    Args:
        symbol (str): The symbol for which to retrieve the 'from' timestamp.

    Returns:
        int: The calculated 'from' timestamp.
    """
    history = pd.read_csv('summary.csv')
    history = history[history['symbol'] == symbol]
    if history.shape[0] > 0:
        return max(history['to']) + 1
    else:
        return int(time.time()) - 8053600  # Default 'from' timestamp

def run(i, symbols, _to):
    """
    Run the data fetching process for each symbol.

    Args:
        i (int): Index/iteration count.
        symbols (pd.DataFrame): DataFrame containing symbols to fetch data for.
        _to (int): The 'to' timestamp.
    """
    msg = '{} at {}'.format(i, _to)
    threads = []
    resolutiuon = '1'
    Log(message=msg)
    for index, row in symbols.iterrows():
        symbol = row['symbol']
        _from = retrive_from(symbol=symbol)
        thread = CryptoFetcher(symbol=symbol, resolutiuon=resolutiuon, _from=_from, _to=_to)
        threads.append(thread)
    
    for thread in threads:
        thread.join()
        
    time.sleep(1)

def main():
    symbols = retriveSymbols()
    i = 1
    fm.Login()  

    while True:
        now = int(time.time())
        if now % 300 == 0:  # Every 5 minutes
            run(i=i, symbols=symbols, _to=now)
            i += 1
            Log('{} - retrieve finished'.format(now))
            fm.moveFilesToDataLake(path=FILE_PATH)  
            Log('{} - transfer finished'.format(now))

if __name__ == '__main__':
    main()
