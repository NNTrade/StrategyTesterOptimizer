from __future__ import annotations
from .strategy_wrapper import PyalgotradeStrategyWrapper
from .data_frame_bar_feed import DataFrameBarFeed
from ...config import StrategyId, SimulationConfig, StrategyConfig, TimeFrame
from ...models import SimulationLog
from ...cache import absSimulationLogStorage
from ...abs_trading_simulatior import absTradingSimulatior,DataFrame
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import BarFeed
from pyalgotrade.bar import Frequency
from typing import Dict, Callable

class PyalgotradeTradingSimulator(absTradingSimulatior):
    class Builder:
        def __init__(self):
            self.report_storage = None
            self.data_source = None
            self.func:Callable[[BarFeed, StrategyConfig],PyalgotradeStrategyWrapper]|None = None
        def set_report_storage(self, report_storage: absSimulationLogStorage | None) -> PyalgotradeTradingSimulator.Builder:
            self.report_storage = report_storage
            return self

        def set_data_source(self, data_source: Dict[str, DataFrame])->PyalgotradeTradingSimulator.Builder:
            self.data_source = data_source
            return self
        def set_str_build_func(self, func:Callable[[BarFeed, StrategyConfig],PyalgotradeStrategyWrapper])->PyalgotradeTradingSimulator.Builder:
            self.str_build_func = func
            return self
        def build(self)->PyalgotradeTradingSimulator:
            if self.str_build_func is None:
                raise AttributeError("str_build_func must be setted", "str_build_func", self.str_build_func)
            if self.data_source is None:
                raise AttributeError("Data source must be setted", "data_source", self.data_source)
            
            return PyalgotradeTradingSimulator(self.data_source, self.str_build_func, self.report_storage)

    def __init__(self, data_source: Dict[str, DataFrame],
                 str_build_func: Callable[[BarFeed, StrategyConfig],PyalgotradeStrategyWrapper ],
                 report_storage: absSimulationLogStorage | None = None) -> None:
        super().__init__(data_source,report_storage, "PyalgotradeTradingSimulator")
        self.__str_build_func = str_build_func

    @property
    def strategy_id(self) -> StrategyId:
        return StrategyId("Example Strategy", "v1")

    def _run(self, run_config: SimulationConfig, alias_data:Dict[str,DataFrame]) -> SimulationLog:
        # Load the bar feed from the CSV file

        frequency = self.__map_frequency(run_config.candle_data_set_config.step_timeframe)

        self._logger.info("Load DataFrameBarFeed")
        feed = DataFrameBarFeed(frequency)
        for stock_alias, stock_cfg in run_config.candle_data_set_config.stocks.items():
            feed.addBarsFromDataFrame(stock_alias, alias_data[stock_alias])

        # Evaluate the strategy with the feed's bars.
        self._logger.info("Run strategy simulation")
        strategy = self.__str_build_func(feed, run_config.strategy_cfg)

        return strategy.run()

    def __map_frequency(self, step_timeframe:TimeFrame)->int:
        if step_timeframe == TimeFrame.M:
            return Frequency.MONTH
        elif step_timeframe == TimeFrame.W:
            return  Frequency.WEEK
        elif step_timeframe == TimeFrame.D:
            return  Frequency.DAY
        elif step_timeframe == TimeFrame.H or \
             step_timeframe == TimeFrame.H4:
            return  Frequency.HOUR
        elif step_timeframe == TimeFrame.m1 or \
             step_timeframe == TimeFrame.m5 or \
             step_timeframe == TimeFrame.m10 or \
             step_timeframe == TimeFrame.m15 or \
             step_timeframe == TimeFrame.m30:
            return Frequency.MINUTE
        else:
            raise AttributeError(f"Unknown mapping for {step_timeframe}")
