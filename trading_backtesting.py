import queue
from datetime import datetime
from RookieQuant.event import EventType
from RookieQuant.data_handler.CSV_bar_handler import CsvBarDataHandler
from RookieQuant.position_sizer.fixed import FixedPositionSizer
from RookieQuant.risk_manager.NoneRiskManager import NoneRiskManager
from RookieQuant.portfolio_processing.portfolio_handler import PortfolioHandler
from RookieQuant.execution_handler.exchange_simulated import ExchangeSimulatedExecutionHandler
from RookieQuant.statistics_report.BasicStatistics import BasicStatisticsReport



class TradingBacktesting(object):

    def __init__(
        self, strategy, tickers,
        equity, start_time, end_time, events_queue,
        data_handler=None, portfolio_handler=None,
        position_sizer=None, execution_handler=None,
        risk_manager=None, statistics=None,
        title=None, benchmark=None
    ):

        self.strategy = strategy
        self.tickers = tickers
        self.equity = equity
        self.start_time = start_time
        self.end_time = end_time
        self.events_queue = events_queue
        self.data_handler = data_handler
        self.portfolio_handler = portfolio_handler
        self.execution_handler = execution_handler
        self.position_sizer = position_sizer
        self.risk_manager = risk_manager
        self.statistics = statistics
        self.title = title
        self.benchmark = benchmark
        self._config_settings()
        self.cur_time = None
    
    def _config_settings(self):

        if self.data_handler is None:
            self.data_handler = CsvBarDataHandler(
            csv_dir="H:\Github\RookieQuant\data",
            events_queue=self.events_queue,
            init_tickers=self.tickers,
            start_time=self.start_time,
            end_time=self.end_time
            )

        if self.position_sizer is None:
            self.position_sizer = FixedPositionSizer()

        if self.risk_manager is None:
            self.risk_manager = NoneRiskManager()

        if self.portfolio_handler is None:
            self.portfolio_handler = PortfolioHandler(
                self.equity, 
                self.events_queue,
                self.data_handler, 
                self.position_sizer, 
                self.risk_manager
            )

        if self.execution_handler is None:
            self.execution_handler = ExchangeSimulatedExecutionHandler(
                self.events_queue,
                self.data_handler
            )

        #statistics_report model to be added latter
        if self.statistics is None:
            self.statistics = BasicStatisticsReport(
                self.portfolio_handler
            )
    

    def _continue_loop_condition(self):
        return self.data_handler.continue_backtest

    def _run_backtesting(self):
        while self._continue_loop_condition():
            try:
                event = self.events_queue.get(False)
            except queue.Empty:
                self.data_handler.stream_next()
            else:
                if event is not None:
                    if(
                        event.type == EventType.TICK or
                        event.type == EventType.BAR
                    ):

                        self.strategy.calculate_signals(event)
                        self.portfolio_handler.update_portfolio_value()
                        self.statistics.update(event.time, self.portfolio_handler)

                    elif event.type == EventType.SIGNAL:
                        self.portfolio_handler.on_signal(event)
                    elif event.type == EventType.ORDER:
                        self.execution_handler.execute_order(event)
                    elif event.type == EventType.FILL:
                        self.portfolio_handler.on_fill(event)
                else:
                    raise NotImplemented("Unsupported event.type '%s'" % event.type)

    def start_trading(self):

        self._run_backtesting()
        results = self.statistics.get_results()
        print("---------------------------------")
        print("Backtest complete.")
        print(results['drawdowns'])
        print("Sharpe Ratio: %0.2f" % results["sharpe"])
        print("Max Drawdown: %0.2f" % results["max_drawdown"])
        print(
            "Max Drawdown: %0.2f%%" % (
                results["max_drawdown_pct"]
            )
        )