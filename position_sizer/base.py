from abc import ABCMeta, abstractmethod

class AbstractPositionSizer(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def size_order(self, portfolio, initial_order):


        raise NotImplementedError("Should implement size_order()")