from RookieQuant.execution_handler.base import AbstractExecutionHandler
from RookieQuant.event import (FillEvent, EventType)


class ExchangeSimulatedExecutionHandler(AbstractExecutionHandler):

    def __init__(self, events_queue, data_handler, compliance=None):

        self.events_queue = events_queue
        self.data_handler = data_handler
        self.compliance = compliance

    
    #only commission considered 
    #more fees to be made future
    def cal_exchange_commission(self, quantity, fill_price):

        commission = max(
            5, 0.001 * fill_price * quantity
        )
        return commission


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
                close_price = self.data_handler.get_last_close(ticker)
                fill_price = close_price

            exchange = "China"
            commission = self.cal_exchange_commission(quantity, fill_price)
            
            fill_event = FillEvent(
                timestamp, ticker,
                action, quantity,
                exchange, fill_price,
                commission
            )

            self.events_queue.put(fill_event)
            


        

    

