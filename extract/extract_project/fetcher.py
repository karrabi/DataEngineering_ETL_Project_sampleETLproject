from threading import Thread
import pandas as pd
import finnhub
from logger import Log



finnhub_client = finnhub.Client(api_key='cak8puqad3ier73m1g30')
finnhub_client.DEFAULT_TIMEOUT=100
FILE_PATH = 'files/'

class CryptoFetcher(Thread):
    def __init__(self, symbol, resolutiuon, _from, _to) -> None:
        super().__init__()
        self.symbol = symbol
        self.resolutiuon = resolutiuon
        self._from = _from
        self._to = _to - 60
        self.start()
        
    def run(self) -> None:
        result = {}
        count = 0
        symbol_str = self.symbol.replace(':', '-')
        try:
            result = finnhub_client.crypto_candles(self.symbol, self.resolutiuon, self._from, self._to)
            result_status = result['s']
            
            if result_status == 'no_data':
                summary = {
                    'at': self._to,
                    'from': self._from,
                    'to': self._to,
                    'symbol': self.symbol,
                    'resolution': self.resolutiuon,
                    'result': result_status
                }
            elif result_status == 'ok':
                result_df = pd.DataFrame(result)
                max_result_timestamp = max(result_df['t'])
                filename = '{}_{}_{}.csv'.format(symbol_str, str(self._to), str(max_result_timestamp))
                result_df.drop(columns=['s'], inplace=True)
                result_df.to_csv('{}{}'.format(FILE_PATH, filename), index=False)
                count = result_df.shape[0]
                summary = {
                    'at': self._to,
                    'from': self._from,
                    'to': max_result_timestamp,
                    'symbol': self.symbol,
                    'resolution': self.resolutiuon,
                    'result': result_status
                }
            pd.DataFrame(summary, index=[0]).to_csv('summary.csv', index=False, header=False, mode='a')
            Log('{} new records recieved for symbol:{}'.format(count, symbol_str))
            # print('Symbol:{} Done'.format(symbol_str))
        except finnhub.FinnhubAPIException as e:
            Log(e.status_code)
            Log(e.message)
        except Exception as e:
            Log(e)
    
    
