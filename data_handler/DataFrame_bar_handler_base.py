import pandas as pd
from abc import ABCMeta, abstractmethod

from RookieQuant.data_handler.base import BarDataHandlerBase
from RookieQuant.event import BarEvent


class DataFrameDataHandler(BarDataHandlerBase):

    __metaclass__ = ABCMeta

    def __init__(self, events_queue, init_tickers,
                 start_time, end_time, period,
                 calc_adj_returns
                 ):
        self.continue_backtest = True
        self.events_queue = events_queue
        self.init_tickers = init_tickers
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.calc_adj_returns = calc_adj_returns
        self.tickers = {}
        self.tickers_data = {}
        if init_tickers is not None:
            for ticker in init_tickers:
                self.subscribe_ticker(ticker)
        self.bar_stream = self._merge_sort_ticker_data()
        if self.calc_adj_returns:
            self.adj_close_returns = []

    @abstractmethod
    def get_dataframe_bar_data(self, ticker):

        raise NotImplementedError("Should get dataframe bar data")

    def subscribe_ticker(self, ticker):

        if ticker not in self.tickers:
            try:
                self.get_dataframe_bar_data(ticker)
                dft = self.tickers_data[ticker]
                row0 = dft.iloc[0]

                close = row0["Close"]
                adj_close = row0["Adj Close"]

                ticker_prices = {
                    "close": close,
                    "adj_close": adj_close,
                    "timestamp": dft.index[0]
                }
                self.tickers[ticker] = ticker_prices

            except OSError:
                print(
                    "Could not subscribe ticker %s "
                    "as no data found for pricing." % ticker
                )
        else:
            print(
                "Could not subscribe ticker%s "
                "as is already subscribed." % ticker
            )

    def _merge_sort_ticker_data(self):

        df = pd.concat(self.tickers_data.values()).sort_index()
        start = None
        end = None
        if self.start_time is not None:
            start = df.index.searchsorted(self.start_time)
        if self.end_time is not None:
            end = df.index.searchsorted(self.end_time)

        df['colFromIndex'] = df.index
        df = df.sort_values(by=["colFromIndex", "Ticker"])
        if start is None and end is None:
            return df.iterrows()
        elif start is not None and end is None:
            return df.ix[start:].iterrows()
        elif start is None and end is not None:
            return df.ix[:end].iterrows()
        else:
            return df.ix[start:end].iterrows()

    def _create_event(self, index, ticker, row):

        period = self.period
        open_price = row["Open"]
        high_price = row["High"]
        low_price = row["Low"]
        close_price = row["Close"]
        adj_close_price = row["Adj Close"]
        volume = int(row['Volume'])
        bev = BarEvent(
            ticker, index, period,
            open_price, high_price, low_price, close_price,
            volume, adj_close_price
        )

        return bev

    def _store_event(self, event):

        ticker = event.ticker
        self.tickers[ticker]["close"] = event.close_price
        self.tickers[ticker]["adj_close"] = event.adj_close_price
        self.tickers[ticker]["timestamp"] = event.time

    def stream_next(self):
        try:
            index, row = next(self.bar_stream)
        except StopIteration:
            self.continue_backtest = False
            return

        ticker = row["Ticker"]

        bev = self._create_event(index, ticker, row)

        self._store_event(bev)

        self.events_queue.put(bev)