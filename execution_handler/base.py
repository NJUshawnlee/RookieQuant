from abc import ABCMeta, abstractmethod


class AbstractExecutionHandler(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):

        raise NotImplementedError("Should implement execute_order()")