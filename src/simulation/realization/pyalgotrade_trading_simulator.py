from __future__ import annotations

from src.common.candle_data_set_config import CandleDataSetConfig
from src.simulation.config.strategy_config import StrategyConfig
from ..config import StrategyId, SimulationConfig
from ..models import SimulationLog
from ..cache import absSimulationLogStorage
from ..abs_trading_simulatior import absTradingSimulatior
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import BarFeed, bar, GenericRowParser
from pyalgotrade.bar import Frequency
from typing import Dict
import pandas as pd
from pyalgotrade import strategy

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

    def __init__(self, frequency:Frequency, timezone=None, maxLen=None, col_names_map:Dict[str,str]= {
            "datetime": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
            "adj_close": "Adj Close",
        }):
        super(DataFrameBarFeed, self).__init__(frequency, maxLen)
        self.__timezone = timezone
        # Assume bars don't have adjusted close. This will be set to True after
        # loading the first file if the adj_close column is there.
        self.__haveAdjClose = False

        self.__barClass = bar.BasicBar

        self.__dateTimeFormat = "%Y-%m-%d"
        self.__columnNames = {
            "datetime": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
            "adj_close": "Adj Close",
        }
        # self.__dateTimeFormat expects time to be set so there is no need to
        # fix time.
        self.setDailyBarTime(None)

    def barsHaveAdjClose(self):
        return self.__haveAdjClose

    def setNoAdjClose(self):
        self.__columnNames["adj_close"] = None
        self.__haveAdjClose = False

    def setColumnName(self, col, name):
        self.__columnNames[col] = name

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
            self.__columnNames, self.__dateTimeFormat, self.getDailyBarTime(), self.getFrequency(),
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
        for row in dataframe.to_dict("records"):
            row[self.__columnNames["datetime"]] = str(
                row[self.__columnNames["datetime"]])
            bar_ = parse_bar(row)
            if bar_ is not None and (self.getBarFilter() is None or self.getBarFilter().includeBar(bar_)):
                loadedBars.append(bar_)

        self.addBarsFromSequence(instrument, loadedBars)

        if rowParser.barsHaveAdjClose():
            self.__haveAdjClose = True
        elif self.__haveAdjClose:
            raise Exception(
                "Previous bars had adjusted close and these ones don't have.")

class PyalgotradeStrategyWrapper(strategy.BacktestingStrategy):
    def __init__(self, barFeed, candle_data_set_config:CandleDataSetConfig, strategy_config:StrategyConfig, cash_or_brk=1000000):
        super().__init__(barFeed, cash_or_brk)
        self._candle_data_set_config = candle_data_set_config
        self._strategy_config = strategy_config

class PyalgotradeTradingSimulator(absTradingSimulatior):
    class Builder:
        def __init__(self):
            self.report_storage = None
        
        def set_report_storage(self, report_storage: absSimulationLogStorage | None)->PyalgotradeTradingSimulator.Builder:
            self.report_storage = report_storage
            return self

        def set_bar_feed_conf(self, 
                              frequency:Frequency, 
                              date_col:str = "Date", 
                              open_col:str="Open",
                              high_col:str="High",
                              low_col:str="Low",
                              close_col:str="Close",
                              volume_col:str="Volume",
                              adj_close:str="Adj Close"):
            return None  

    def __init__(self,  quote_data:Dict[str, pd.DataFrame], frequency:Frequency,
                 report_storage: absSimulationLogStorage | None = None) -> None:
        super().__init__(report_storage, "PyalgotradeTradingSimulator")
        self.__quote_data = quote_data
        self.__frequency = frequency

    @property
    def strategy_id(self)->StrategyId:
        return StrategyId("Example Strategy", "v1")
    
    def _run(self, run_config: SimulationConfig)->SimulationLog:
        # Load the bar feed from the CSV file
        
        self._logger.info("Load DataFrameBarFeed")
        feed = DataFrameBarFeed(self.__frequency)
        for stock_name,stock_cfg in run_config.candle_data_set_config.stocks.items():
            feed.addBarsFromDataFrame(stock_name, run_config.period.filter_df(self.__quote_data[stock_cfg.ticker]))

        signal_delta = run_config.strategy_cfg["delta"]
        # Evaluate the strategy with the feed's bars.
        self._logger.info("Run strategy simulation")
        strategy = PyalgotradeStrategyWrapper(feed, run_config.candle_data_set_config, run_config.strategy_cfg)
        strategy.run()
        return SimulationLog(myStrategy.cap_log,myStrategy.deal_list)