from numpy import sign


class Position(object):
    def __init__(
        self, action, ticker, init_quantity,
        init_price, init_commission,
        bid, ask
    ):

        self.action = action
        self.ticker = ticker
        self.quantity = init_quantity
        self.init_price = init_price
        self.init_commission = init_commission

        self.realized_pnl = 0
        self.unrealized_pnl = 0

        self.buys = 0
        self.sells = 0
        self.avg_bot = 0
        self.avg_sld = 0
        self.total_bot = 0
        self.total_sld = 0
        self.total_commission = init_commission

        self._calculate_initial_value()
        self.update_market_value(bid, ask)
    
    def _calculate_initial_value(self):

        if self.action == "BOT":
            self.buys = self.quantity
            self.avg_bot = self.init_price
            self.total_bot = self.buys * self.avg_bot
            self.avg_price = (self.init_price * self.quantity + self.init_commission) / self.quantity
            self.cost.basis  = self.quantity * self.avg_price
        else: # action == "SLD"
            self.sells = self.quantity
            self.avg_sld = self.init_price
            self.total_sld = self.sells * self.avg_sld
            self.avg_price = (self.init_price * self.quantity - self.init_commission) / self.quantity
            self.cost_basis = -self.quantity * self.avg_price
        self.net = self.buys - self.sells
        self.net_total = self.total_sld - self.total_bot
        self.net_incl_comm = self.net_total - self.init_commission
    
    def update_market_value(self, bid, ask):

        midpoint = (bid + ask) / 2
        self.market_value = self.quantity * midpoint * sign(self.net)
        self.unrealized_pnl = self.market_value - self.cost_basis

    
    def transact_shares(self, action, quantity, price, commission):


        self.total_commission += commission

        if action == "BOT":
            self.avg_bot = (
                self.avg_bot * self.buys + price * quantity
            ) / (self.buys + quantity)
            if self.action != "SLD":
                self.avg_price = (
                    self. avg_price * self.buys +
                    price * quantity + commission
                ) / (self.buys + quantity)

            elif  self.action == "SLD":
                self.realized_pnl += quantity*(
                self.avg_price - price
                ) - commission
            self.buys += quantity
            self.total_bot = self.buys * self.avg_bot

        # action == "SLD"
        else:
            self.avg_sld = (
                self.avg_sld * self.sells + price * quantity 
            ) / (self.sells + quantity)
            if self.action != "BOT":
                self.avg_price = (
                    self.avg_price * self.sells + 
                    price * quantity -commission
                ) / (self.sells + quantity)
            elif self.action == "BOT":
                self.realized_pnl += quantity*(
                    price - self.avg_price
                ) - commission
            self.sells += quantity
            self.total_sld = self.sells * self.avg_sld

        self.net = self.buys - self.sells
        self.quantity =  self.net
        self.net_total = self.total_sld - self.total_bot
        self.net_incl_comm = self.net_total - self.total_commission

        self.cost_basis  = self.quantity * self.avg_price
        


    