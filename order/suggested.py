class SuggestedOrder(object):

    def __init__(self, ticker, action, quantity=0):

        self.ticker = ticker
        self.action = action
        self.quantity = quantity