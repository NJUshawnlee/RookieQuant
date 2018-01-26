from RookieQuant.risk_manager.base import AbstractRiskManager
from RookieQuant.event import OrderEvent

class NoneRiskManager(AbstractRiskManager):

    def refine_orders(self, portfolio, sized_order):

        
        order_event = OrderEvent(

            sized_order.ticker,
            sized_order.action,
            sized_order.quantity
        )

        return [order_event]

    
