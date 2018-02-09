import queue
import datetime
from RookieQuant.strategy.base import AbstractStrategy
from RookieQuant.event import SignalEvent, EventType
from RookieQuant.trading_backtesting import TradingBacktesting
from RookieQuant.data_handler.SQL_bar_handler import SqlBarDataHandler
from RookieQuant.position_sizer.common_stock_size_checker import CommonStockChecker
from RookieQuant.portfolio_processing.portfolio_handler import PortfolioHandler

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
            base_quantity=1
    ):
        super().__init__(ticker, events_queue)
        self.base_quantity = base_quantity
        self.bars = 0

    def calculate_signals(self, event):

        if (
            # will be corrected when tick data_handler to be added latter
            event.type is EventType.BAR
            and event.ticker == self.tickers[0]
        ):
            if self.bars < 1:
                signal = SignalEvent(
                    self.tickers[0], "BOT",
                    suggested_quantity=self.base_quantity
                )
                self.events_queue.put(signal)
                self.invested = True
            self.bars += 1

        # elif (
        #     # will be corrected when tick data_handler to be added latter
        #     event.type is EventType.BAR
        #     and event.ticker == self.tickers[1]
        # ):
        #     if self.bars < 1:
        #         signal = SignalEvent(
        #             self.tickers[1], "BOT",
        #             suggested_quantity=self.base_quantity
        #         )
        #         self.events_queue.put(signal)
        #         self.invested = True
        #     self.bars += 1


def run(tickers):

    title = ['Buy and Hold Example on %s' % tickers[0]]
    initial_equity = 10000
    start_date = datetime.datetime(2000, 1, 1)
    end_date = datetime.datetime(2018, 2, 2)

    events_queue = queue.Queue()
    strategy = BuyAndHoldStrategy(tickers, events_queue)
    # data_handler = SqlBarDataHandler(sws_sql_config, sws_sql_cmd,
    #                                  '2017/01/01', '2018/02/02',
    #                                  events_queue, tickers,
    #                                  start_date, end_date
    #                                  )
    position_sizer = CommonStockChecker()

    backtest = TradingBacktesting(
         strategy, tickers, initial_equity,
         start_date, end_date, events_queue, title=title,
         position_sizer=position_sizer, dir="H:\Github\RookieQuant\data", print_trading_log=True)
    # backtest = TradingBacktesting(
    #     strategy, tickers, initial_equity,
    #     start_date, end_date, events_queue, data_handler=data_handler,
    #     position_sizer=position_sizer, title=title
    # )

    results = backtest.start_trading()
    return results


if __name__ == "__main__":

    tickers = ["SP500"]
    run(tickers)

