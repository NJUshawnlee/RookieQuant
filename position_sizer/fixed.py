import sys
sys.path.append("..")

from position_sizer.base import AbstractPositionSizer


class FixedPositionSizer(AbstractPositionSizer):

    def __init__(self, default_quantity=100):
        self.default_quantity = default_quantity

    def size_order(self, portfolio, initial_order):

        return initial_order
