from enum import Enum


EventType = Enum("EventType", "TICK BAR SIGNAL ORDER FILL SENTIMENT")


class Event(object):
    
    @property
    def typename(self):
        return self.type.name


class TickEvent(Event):
    pass

class BarEvent(Event):
    
    def __init__(
        self,  ticker, time, period,
        open_price, high_price, low_price,
        close_price, volume, adj_close_price=None
    ):
        self.type = EventType.BAR
        self.ticker = ticker
        self.time = time
        self.period = period
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.adj_close_price = adj_close_price    

class SignalEvent(Event):
    
    def __init__(self, ticker, action, suggested_quantity=None):

        self.type = EventType.SIGNAL
        self.ticker = ticker
        self.action = action
        self.suggested_quantity = suggested_quantity

class OrderEvent(Event):
    
    def __init__(self, ticker, action, quantity):

        self.type = EventType.ORDER
        self.ticker = ticker
        self.action = action
        self.quantity = quantity

    def print_order(self):
        
        print(
            "Order: Ticker=%s, Action=%s, Quantity=%s" % (
                self.ticker, self.action, self.quantity
            )
        )


class FillEvent(Event):
    
    def __init__(
        self, timestamp, ticker,
        action, quantity,
        exchange, price,
        commission
    ):

        self.type =EventType.FILL
        self.timestamp = timestamp
        self.ticker = ticker
        self.action = action
        self.quantity = quantity
        self.exchange = exchange
        self.price = price
        self.commission = commission

