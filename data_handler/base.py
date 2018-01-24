from abc import ABCMeta



class DataHandlerBase(object):

    __metaclass__ = ABCMeta

    def unsubscribe_ticker(self, ticker):
        pass

    def get_last_timestamp(self, ticker):
        pass

    pass

class BarDataHandlerBase(DataHandlerBase):

    def istick(self):
        return False

    def isbar(self):
        return True

    def get_last_close(self, ticker):
        
        if ticker in self.tickers:
            close_price = self.tickers[ticker]["close"]
        else:
            print(
                "Close price for ticker %s in not"
                "available from BarDataHandler." % ticker
            )
        return None

    def _store_event_price(self, event):
        pass

    def _store_event_return(self, event):
        pass

    def _store_event_volume(self, event):
        pass

    def _store_event_multiple_price(self, event):
        pass

    def _store_event_multiple_return(self, event):
        pass

    def _store_event_multiple_volume(self, event):
        pass

class TickDatahandler(DataHandlerBase):
    
    def istick(self):
        return True

    def isbar(self):
        return False
