from RookieQuant.order.suggested import SuggestedOrder
from RookieQuant.portfolio_processing.portfolio import Portfolio


class PortfolioHandler(object):
    def __init__(
        self, initial_cash, events_queue, 
        data_handler, position_sizer, risk_manager

    ):
        
        self.initial_cash = initial_cash
        self.events_queue = events_queue
        self.data_handler = data_handler
        self.position_sizer = position_sizer
        self.risk_manager = risk_manager
        self.portfolio = Portfolio(data_handler, initial_cash)

    def _create_order_from_signal(self, signal_event):

        if signal_event.suggested_quantity is None:
            quantity = 0
        else:
            quantity = signal_event.suggested_quantity
        order = SuggestedOrder(
            signal_event.ticker,
            signal_event.action,
            quantity=quantity
        )
        return order


    def _place_orders_onto_queue(self, order_list):
        
        for order_event in order_list:
            self.events_queue.put(order_event)

    def _convert_fill_to_portfolio_update(self, fill_event):
        

        action = fill_event.action
        ticker = fill_event.ticker
        quantity = fill_event.quantity
        price = fill_event.price
        commission = fill_event.commission

        self.portfolio.transact_position(
            action, ticker, quantity,
            price, commission
        )

    def on_signal(self, signal_event):

        initial_order = self._create_order_from_signal(signal_event)

        sized_order = self.position_sizer.size_order(
            self.portfolio, initial_order
        )

        order_events = self.risk_manager.refine_orders(
            self.portfolio, sized_order
        )
        self._place_orders_onto_queue(order_events)

    def on_fill(self, fill_event):

        self._convert_fill_to_portfolio_update(fill_event)     

    def update_portfolio_value(self):

        self.portfolio._update_portfolio()

