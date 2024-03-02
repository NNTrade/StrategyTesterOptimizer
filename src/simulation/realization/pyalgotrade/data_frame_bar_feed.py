import pandas as pd
from NNTrade.common.candle_col_name import CLOSE, HIGH, INDEX, LOW, OPEN, VOLUME
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import BarFeed, GenericRowParser, bar


class DataFrameBarFeed(BarFeed):
    """A BarFeed that loads bars from CSV files that have the following format:
    ::

        Date Time,Open,High,Low,Close,Volume,Adj Close
        2013-01-01 13:59:00,13.51001,13.56,13.51,13.56,273.88014126,13.51001

    :param frequency: The frequency of the bars. Check :class:`pyalgotrade.bar.Frequency`.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.

    .. note::
        * The CSV file **must** have the column names in the first row.
        * It is ok if the **Adj Close** column is empty.
        * When working with multiple instruments:

         * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.
         * If any of the instruments loaded are in different timezones, then the timezone parameter should be set.
    """
    DT_COL_N = "datetime"
    OPEN_COL_N = "open"
    HIGH_COL_N = "high"
    LOW_COL_N = "low"
    CLOSE_COL_N = "close"
    VOLUME_COL_N = "volume"
    ADJ_CLOSE_N = "adj_close"

    DEFAULT_MAP = {
        DT_COL_N: INDEX,
        OPEN_COL_N: OPEN,
        HIGH_COL_N: HIGH,
        LOW_COL_N: LOW,
        CLOSE_COL_N: CLOSE,
        VOLUME_COL_N: VOLUME,
        ADJ_CLOSE_N: None
    }

    def __init__(self, frequency: Frequency|int, timezone=None, maxLen=None):
        super(DataFrameBarFeed, self).__init__(frequency, maxLen)
        self.__timezone = timezone
        # Assume bars don't have adjusted close. This will be set to True after
        # loading the first file if the adj_close column is there.
        self.__haveAdjClose = False

        self.__barClass = bar.BasicBar

        self.__dateTimeFormat = "%Y-%m-%d %H:%M:%S"
        # self.__dateTimeFormat expects time to be set so there is no need to
        # fix time.
        self.setDailyBarTime(None)

    def barsHaveAdjClose(self):
        return self.__haveAdjClose

    def setNoAdjClose(self):
        self.__haveAdjClose = False

    def setDateTimeFormat(self, dateTimeFormat):
        """
        Set the format string to use with strptime to parse datetime column.
        """
        self.__dateTimeFormat = dateTimeFormat

    def setBarClass(self, barClass):
        self.__barClass = barClass

    def addBarsFromDataFrame(self, instrument: str, dataframe: pd.DataFrame, timezone=None, skipMalformedBars=False):
        """Load bars from DataFrame

        Args:
            instrument (str): Instrument identifier
            dataframe (pandas.DataFrame): loaded dataframe
            timezone (pytz timezone, optional): The timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`. Defaults to None.
            skipMalformedBars (bool, optional): True to skip errors while parsing bars. Defaults to False.
        """
        if timezone is None:
            timezone = self.__timezone

        rowParser = GenericRowParser(
            DataFrameBarFeed.DEFAULT_MAP, self.__dateTimeFormat, self.getDailyBarTime(), self.getFrequency(),
            timezone, self.__barClass
        )

        def parse_bar_skip_malformed(row):
            ret = None
            try:
                ret = rowParser.parseBar(row)
            except Exception:
                pass
            return ret

        if skipMalformedBars:
            parse_bar = parse_bar_skip_malformed
        else:
            parse_bar = rowParser.parseBar

        loadedBars = []
        for row in dataframe.reset_index().to_dict("records"):
            row[DataFrameBarFeed.DEFAULT_MAP[DataFrameBarFeed.DT_COL_N]] = str(
                row[DataFrameBarFeed.DEFAULT_MAP[DataFrameBarFeed.DT_COL_N]])
            bar_ = parse_bar(row)
            if bar_ is not None and (self.getBarFilter() is None or self.getBarFilter().includeBar(bar_)):
                loadedBars.append(bar_)

        self.addBarsFromSequence(instrument, loadedBars)

        if rowParser.barsHaveAdjClose():
            self.__haveAdjClose = True
        elif self.__haveAdjClose:
            raise Exception(
                "Previous bars had adjusted close and these ones don't have.")