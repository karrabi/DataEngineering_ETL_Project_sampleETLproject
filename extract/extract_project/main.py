import pandas as pd
import time

from fetcher import CryptoFetcher
from logger import Log
import filemanager as fm

FILE_PATH = 'files/'


def resolveSymbols():
    symbols = pd.read_csv('symbols.csv')
    return symbols


def resolve_from(symbol):
    history = pd.read_csv('summary.csv')
    history = history[history['symbol']==symbol]
    if history.shape[0] > 0:
        return max(history['to']) + 1
    else:
        return int(time.time()) - 8053600
    
    
def run(i, symbols, _to):
    msg = '{} at {}'.format(i, _to)
    threads= []
    resolutiuon = '1' 
    Log(message=msg)
    for index, row in symbols.iterrows():
        symbol = row['symbol']
        _from = resolve_from(symbol=symbol)
        thread = CryptoFetcher(symbol=symbol, resolutiuon=resolutiuon, _from=_from, _to=_to)

        threads.append(thread)
    
    for thread in threads:
        thread.join()
        
    time.sleep(1)


def main():

    symbols = resolveSymbols()
    i = 1
    
    fm.Login()

    while True:
        now = int(time.time())
        if now % 300 == 0:
            run(i=i, symbols=symbols, _to=now)
            i += 1
            Log('{} - retrive finished'.format(now))
            fm.moveFilesToDataLake(path=FILE_PATH)
            Log('{} - transfer finished'.format(now))

if __name__ == '__main__':
    main()
    