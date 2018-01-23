import queue
from .event import EventType
from .data_handler.CSV_bar_handler import CsvBarDataHandler

_continue_loop_condition = 1
def _run_session():
    while _continue_loop_condition:
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
        elif expression:
            pass

