from re import L
from pandas import DataFrame
from NNTrade.common.candle_col_name import CLOSE, HIGH, INDEX, LOW, OPEN, VOLUME
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import BarFeed, GenericRowParser, bar
from pyalgotrade.barfeed import BaseBarFeed
from typing import Dict
from pyalgotrade.technical import ma

class InMemBarFeed(BarFeed):
    def __init__(self, frequency, maxLen=None):
        super().__init__(frequency, maxLen)
    def barsHaveAdjClose(self):
        return False

class CustomValuesWrapper(ma.SMA):
    def __init__(self, dataSeries):
        super().__init__(dataSeries, 1)