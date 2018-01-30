import queue
import datetime
from RookieQuant.strategy.base import AbstractStrategy
from RookieQuant.event import SignalEvent, EventType
from RookieQuant.trading_backtesting import TradingBacktesting
from RookieQuant.data_handler.SQL_bar_handler import SqlBarDataHandler

sws_sql_cmd = '''SELECT [BargainDate],[OpenPrice],[MaxPrice],[MinPrice],[ClosePrice],[BargainAmount],[StockCode]
            FROM [StockBase].[dbo].[Quotation] where StockCode='%s'
            and BargainDate>='%s' and BargainDate<='%s'
            order by StockCode, BargainDate'''

sws_sql_config = '' r'DRIVER={ODBC Driver 13 for SQL Server};' \
                 r''r'SERVER=192.30.1.40;' \
                 r''r'DATABASE=StockBase;' \
                 r''r'UID=du_songsy;' \
                 r''r'PWD=songsy;'  ''

class BuyAndHoldStrategy(AbstractStrategy):

    def __init__(
            self, ticker, events_queue,
            base_quantity=200
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
    start_date = datetime.datetime(2017, 1, 1)
    end_date = datetime.datetime(2017, 12, 31)

    events_queue = queue.Queue()
    strategy = BuyAndHoldStrategy(tickers[0], events_queue)
    data_handler = SqlBarDataHandler(sws_sql_config, sws_sql_cmd,
                                     '2017/01/01', '2017/12/31',
                                     events_queue, tickers,
                                     start_date, end_date
                                     )

    # backtest = TradingBacktesting(
    #     strategy, tickers, initial_equity,
    #     start_date, end_date, events_queue, title=title, dir="H:\Github\RookieQuant\data"
    # )
    backtest = TradingBacktesting(
        strategy, tickers, initial_equity,
        start_date, end_date, events_queue, data_handler, title=title
    )

    results = backtest.start_trading()
    return results


if __name__ == "__main__":

    tickers = ["600516"]
    run(tickers)

