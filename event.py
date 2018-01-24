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
        self,  ticker, time, period
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
    pass

class OrderEvent(Event):
    pass

class FillEvent(Event):
    pass

