from threading import Thread
import pandas as pd
import finnhub
from logger import Log

# Initialize the Finnhub client with your API key
finnhub_client = finnhub.Client(api_key='cak8puqad3ier73m1g30')
finnhub_client.DEFAULT_TIMEOUT = 100
FILE_PATH = 'files/'

# Define a class for fetching crypto data using threading
class CryptoFetcher(Thread):
    def __init__(self, symbol, resolutiuon, _from, _to) -> None:
        """
        Initialize the CryptoFetcher class.

        Args:
            symbol (str): The symbol of the cryptocurrency.
            resolutiuon (str): The resolution of the data (e.g., 'D' for daily).
            _from (int): The starting timestamp for data retrieval.
            _to (int): The ending timestamp for data retrieval.
        """
        super().__init__()
        self.symbol = symbol
        self.resolutiuon = resolutiuon
        self._from = _from
        self._to = _to - 60  # Adjusted end timestamp to ensure data before _to is fetched
        self.start()

    def run(self) -> None:
        """
        Method executed when the thread is started. Fetches crypto data and processes it.
        """
        result = {}
        count = 0
        symbol_str = self.symbol.replace(':', '-')
        try:
            # Fetch crypto data from Finnhub API
            result = finnhub_client.crypto_candles(self.symbol, self.resolutiuon, self._from, self._to)
            result_status = result['s']

            if result_status == 'no_data':
                # Prepare summary for no data case
                summary = {
                    'at': self._to,
                    'from': self._from,
                    'to': self._to,
                    'symbol': self.symbol,
                    'resolution': self.resolutiuon,
                    'result': result_status
                }
            elif result_status == 'ok':
                # Process and save fetched data
                result_df = pd.DataFrame(result)
                max_result_timestamp = max(result_df['t'])
                filename = '{}_{}_{}.csv'.format(symbol_str, str(self._to), str(max_result_timestamp))
                result_df.drop(columns=['s'], inplace=True)
                result_df.to_csv('{}{}'.format(FILE_PATH, filename), index=False)
                count = result_df.shape[0]
                # Prepare summary for successful data fetch
                summary = {
                    'at': self._to,
                    'from': self._from,
                    'to': max_result_timestamp,
                    'symbol': self.symbol,
                    'resolution': self.resolutiuon,
                    'result': result_status
                }
            # Append the summary to a summary file
            pd.DataFrame(summary, index=[0]).to_csv('summary.csv', index=False, header=False, mode='a')
            Log('{} new records received for symbol:{}'.format(count, symbol_str))
            # print('Symbol:{} Done'.format(symbol_str))
        except finnhub.FinnhubAPIException as e:
            # Handle Finnhub API exceptions
            Log(e.status_code)
            Log(e.message)
        except Exception as e:
            # Handle other exceptions
            Log(e)
