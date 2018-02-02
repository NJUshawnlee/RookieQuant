from abc import ABCMeta, abstractmethod
import numpy as np


class AbstractStrategy(object):

    __metaclass__ = ABCMeta

    def __init__(
            self, tickers, events_queue
    ):

        self.tickers = tickers
        self.events_queue = events_queue
        self.time = None
        self.num_of_tickers = len(tickers)
        self.latest_prices = np.full(self.num_of_tickers, -1.0)
        self.invested = False

    @abstractmethod
    def calculate_signals(self, event):

        raise NotImplementedError("Should implement calculate_signals()")

    def _set_correct_time_and_price(self, event):

        if self.time is None:
            self.time = event.time

        price = event.adj_close_price

        if event.time == self.time:
            for i in range(self.num_of_tickers):
                if event.ticker == self.tickers[i]:
                    self.latest_prices[i] = price
                    break

        else:
            self.time = event.time
            self.bars_elapsed += 1
            self.latest_prices = np.full(self.num_of_tickers, -1.0)
            for i in range(self.num_of_tickers):
                if event.ticker == self.tickers[i]:
                    self.latest_prices[i] = price
                    break
