import queue
import datetime
from RookieQuant.strategy.base import AbstractStrategy
from RookieQuant.event import SignalEvent, EventType
from RookieQuant.trading_backtesting import TradingBacktesting


class BuyAndHoldStrategy(AbstractStrategy):

    def __init__(
            self, ticker, events_queue,
            base_quantity=1
    ):
        self.ticker = ticker
        self.events_queue = events_queue
        self.base_quantity = base_quantity
        self.bars = 0
        self.invested = False

    def calculate_signals(self, event):

        if (
            # will be corrected when tick data_handler to be added latter
            event.type is EventType.BAR and
            event.ticker == self.ticker
        ):
            if not self.invested and self.bars == 0:
                signal = SignalEvent(
                    self.ticker, "BOT",
                    suggested_quantity=self.base_quantity
                )
                self.events_queue.put(signal)
                self.invested = True
            self.bars += 1


def run(tickers):

    title = ['Buy and Hold Example on %s' % tickers[0]]
    initial_equity = 5000
    start_date = datetime.datetime(2000, 1, 5)
    end_date = datetime.datetime(2014, 1, 1)

    events_queue = queue.Queue()
    strategy = BuyAndHoldStrategy(tickers[0], events_queue)

    backtest = TradingBacktesting(
        strategy, tickers, initial_equity,
        start_date, end_date, events_queue, title=title
    )

    results = backtest.start_trading()
    return results


if __name__ == "__main__":

    tickers = ["SP500"]
    run(tickers)

