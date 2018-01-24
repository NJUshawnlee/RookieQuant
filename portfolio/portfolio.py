from ..position.position import Position


class Portfolio(object):
    def __init__(self, data_handler, cash):

        self.data_handler = data_handler
        self.init_cash = cash
        self.equity = cash
        self.cur_cash = cash
        self.positions = {}
        self.closed_positions = []
        self.realised_pnl = 0

    def _update_portfolio(self, event):

        self.unrealised_pnl = 0
        # do some corrections here 
        self.equity = 0 
        self.equity += self.cur_cash
        #so high updating  frequency here
        #and can be reduced upon finishing the framework 
        for ticker in self.positions:
            pt = self.positions[ticker]
            # tick data_handler to be made later
            if self.data_handler.istick():
                pass
            else:
                close_price = self.data_handler.get_last_close(ticker)
                bid = close_price
                ask = close_price
            pt.update_market_value(bid, ask)
            self.unrealised_pnl += pt.unrealised_pnl
            self.equity += (
                pt.market_value - pt.cost_basis + pt.realised_pnl
            )

    def  _add_position(
        self, action, ticker,
        quantity, price, commission
    ):
        if ticker not in self.positions:
            # tick data_handler to be made later
            if self.data_handler.istick():
                pass
            else:
                close_price = self.data_handler.get_last_close(ticker)
                bid = close_price
                ask = close_price
            position = Position(
                action, ticker, quantity, 
                price, commission, bid, ask
            )
            self.positions[ticker] = position
            self._update_portfolio()
        else:
            print(
                "Ticker %s is already in the positions list. "
                "Could not add a new position." % ticker
            )
            

    def _modify_position(
        self, action, ticker,
        quantity, price, commission
    ):
        
        if ticker in self.positions:
            self.positions[ticker].transact_shares(
                action, quantity, price, commission
            )
            # tick data_handler to be made later
            if self.data_handler.istick():
                pass
            else:
                close_price = self.data_handler.get_last_close(ticker)
                bid = close_price
                ask = close_price
            self.positions[ticker].update_market_value(bid, ask)

            if self.positions[ticker].quantity == 0:
                closed = self.positions.pop(ticker)
                self.realised_pnl += closed.realised_pnl
                self.closed_positions.append(closed)
            
            self._update_portfolio()

        else:
            print(
                "Ticker %s not in the current position list. "
                "Could not modify a current position." % ticker
            )

    def transact_position(
        self, action, ticker,
        quantity, price, commission
    ):

        if action == "BOT":
            self.cur_cash -= ((quantity * price) + commission)
        elif action == "SLD":
            self.cur_cash += ((quantity * price) - commission)


        if ticker not in self.positions:
            self._add_position(
                action, ticker, quantity,
                price, commission
            )

        else:
            self._modify_position(
                action, ticker, quantity,
                price, commission
            )



    

