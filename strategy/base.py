from abc import ABCMeta, abstractmethod


class AbstractStrategy(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_signals(self, event):

        raise NotImplementedError("Should implement calculate_signals()")
