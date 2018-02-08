import os
import pandas as pd

from RookieQuant.data_handler.DataFrame_bar_handler_base import DataFrameDataHandler


class CsvBarDataHandler(DataFrameDataHandler):

    def __init__(
        self,  csv_dir, events_queue, init_tickers,
        start_time=None, end_time=None, period=86400,
        record_hist_prices=False, record_hist_returns=False, record_hist_volume=False
    ):
        self.csv_dir = csv_dir
        super().__init__(events_queue, init_tickers, start_time, end_time,
                         period, record_hist_prices, record_hist_returns, record_hist_volume)

        self.continue_backtest = True
        self.tickers = {}
        self.tickers_data = {}
        if init_tickers is not None:
            for ticker in init_tickers:
                self.subscribe_ticker(ticker)
        self.bar_stream = self._merge_sort_ticker_data()

    def _open_ticker_price_csv(self, ticker):
        
        ticker_path = os.path.join(self.csv_dir, "%s.csv" % ticker)
        self.tickers_data[ticker] = pd.io.parsers.read_csv(
            ticker_path, header=0, parse_dates=True,
            index_col=0, names=(
                "Date", "Open", "High", 'Low',
                "Close", "Volume", "Adj Close"
            )
        )
        self.tickers_data[ticker]["Ticker"] = ticker

    def get_dataframe_bar_data(self, ticker):

        self._open_ticker_price_csv(ticker)
