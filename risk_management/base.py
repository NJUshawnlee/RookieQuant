from abc import ABCMeta, abstractmethod


class AbstractRiskManager(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def refine_orders(self, portfolio, sized_order):

        raise NotImplementedError("Should implement refine_orders()")
        