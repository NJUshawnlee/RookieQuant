from abc import ABCMeta



class DataHandlerBase(object):

    __metaclass__ = ABCMeta

    pass

class BarDataHandlerBase(DataHandlerBase):
    pass

class TickDatahandler(DataHandlerBase):
    pass
