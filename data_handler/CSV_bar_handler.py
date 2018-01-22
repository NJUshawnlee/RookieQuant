import os

import pandas as pd 

from .base import BarHandlerBase

class CsvBarDataHandler(BarHandlerBase):

    def __init__(
        self, csv_dir, events_queue,
        init_tickers=None，
        start_time=None, end_time=None,
        calc_adj_returns=False
    ):

        self.csv_dir = csv_dir
        self.events_queue = events_queue
        self.continue_backtest = True
        self.tickers = {}
        self.tickers_data = {}
        if init_tickers is not None:
            for ticker in init_tickers:
                self.subscribe_ticker(ticker)
        self.start_time = start_time
        self.end_time = end_time
        self.bar_stream = self._merge_sort_code_data()
        self.calc_adj_returns = calc_adj_returns
        if self.calc_adj_returns:
            self.adj_close_returns = []



    