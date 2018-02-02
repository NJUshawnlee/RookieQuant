from RookieQuant.position_sizer.base import AbstractPositionSizer


class CommonStockChecker(AbstractPositionSizer):

    def __init__(self, default_quantity=100):
        self.default_quantity = default_quantity

    def size_order(self, portfolio, initial_order, data_handler):

        ticker = initial_order.ticker
        if initial_order.action == "BOT":
            price = data_handler.get_last_close(ticker)
            cost = price * initial_order.quantity

            if cost > portfolio.cur_cash:
                raise Exception("There is no enough cash.")
            else:
                return initial_order

        if initial_order.action == "SLD":
            if initial_order.quantity > portfolio.positions[ticker].quantity:
                raise Exception("There are no enough stocks.")
            else:
                return initial_order
