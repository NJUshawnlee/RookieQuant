from RookieQuant.execution_handler.base import AbstractExecutionHandler
from RookieQuant.event import (FillEvent, EventType)
import random

class ExchangeSimulatedExecutionHandler(AbstractExecutionHandler):

    def __init__(self, events_queue, data_handler, compliance=None):

        self.events_queue = events_queue
        self.data_handler = data_handler
        self.compliance = compliance

    
    #only commission considered 
    #more fees to be made future
    def cal_exchange_commission(self, quantity, fill_price, event):

        if event.action == 'BOT':
            commission = max(5, 0.001 * fill_price * quantity)\
                         + max(1, quantity / 1000 * 0.6)
        else:
            commission = max(5, 0.001 * fill_price * quantity
                             ) + max(1, quantity / 1000 * 0.6) + 0.001 * fill_price * quantity

        return commission

    def cal_slippage(self, volatility=0.001):

        pct = random.gauss(0, volatility)
        pct_range = 3 * volatility
        if pct < (-1) * pct_range:
            pct = (-1) * pct_range
        elif pct > pct_range:
            pct = pct_range

        return pct

    def execute_order(self, event):

        if event.type == EventType.ORDER:

            ticker = event.ticker
            timestamp = self.data_handler.get_last_timestamp(ticker)
            action = event.action
            quantity = event.quantity

            # tick data_handler1 to be made later
            if self.data_handler.istick():
                pass
            else:
                open_price = self.data_handler.get_last_open(ticker)
                fill_price = round(open_price * (1 + self.cal_slippage()), 2)

            exchange = "China"
            commission = self.cal_exchange_commission(quantity, fill_price, event)
            
            fill_event = FillEvent(
                timestamp, ticker,
                action, quantity,
                exchange, fill_price,
                commission
            )

            self.events_queue.put(fill_event)
            


        

    

