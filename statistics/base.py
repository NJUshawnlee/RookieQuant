from abc import ABCMeta, abstractmethod

class AbstractStatistics(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):

        raise NotImplementedError("Should implement update()")

    @abstractmethod
    def get_results(self):

        raise NotImplementedError("Should implement get_results()")

    @abstractmethod
    def plot_results(self):

        raise NotImplementedError("Should implement plot_results()")