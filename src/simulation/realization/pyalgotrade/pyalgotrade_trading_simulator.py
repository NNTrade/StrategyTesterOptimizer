from __future__ import annotations
from .strategy_wrapper import StrategyWrapper
from .data_frame_bar_feed import InMemBarFeed,OPEN, HIGH, CLOSE, LOW,VOLUME, CustomValuesWrapper
from ...config import StrategyId, SimulationConfig, StrategyConfig, TimeFrame
from ...models import SimulationLog
from ...cache import absSimulationLogStorage
from ...abs_trading_simulator import absTradingSimulator,DataFrame
from pyalgotrade.bar import Frequency,BasicBar
from pyalgotrade.barfeed.csvfeed import BarFeed
from pyalgotrade.bar import Frequency
from typing import Dict, Callable


class PyalgotradeTradingSimulator(absTradingSimulator):
    def __init__(self, data_source: Dict[str, DataFrame],
                 strategy_wrapper_factory: StrategyWrapper.Factory,
                 report_storage: absSimulationLogStorage | None = None,
                 ) -> None:
        super().__init__(data_source,report_storage, "PyalgotradeTradingSimulator")
        self.__strategy_wrapper_factory = strategy_wrapper_factory
        self.__report_storage = report_storage

    def _run(self, strategy_id:StrategyId, run_config: SimulationConfig, alias_data:Dict[str,DataFrame]) -> SimulationLog:
        # Load the bar feed from the CSV file

        frequency = self.__map_frequency(run_config.candle_data_set_config.step_timeframe)

        self._logger.info("Load DataFrameBarFeed")
        feed = InMemBarFeed(frequency)

        for stock_alias in run_config.candle_data_set_config.stocks.keys():
            data_df = alias_data[stock_alias]
            mask = ~data_df.columns.isin([OPEN, HIGH, CLOSE, LOW,VOLUME])
            BasicBars = []
            for index, row in data_df.iterrows():
                bb = BasicBar(
                        index,      
                        row[OPEN],
                        row[HIGH],            
                        row[LOW],             
                        row[CLOSE],           
                        row[VOLUME],          
                        None,           
                        frequency,        
                        row[mask].to_dict())
                BasicBars .append(bb)
            feed.addBarsFromSequence(stock_alias, BasicBars)    

        # Evaluate the strategy with the feed's bars.
        self._logger.debug("Run strategy simulation")
        strategy = self.__strategy_wrapper_factory.get(strategy_id, feed, run_config.strategy_cfg)

        return strategy.run()

    def __map_frequency(self, step_timeframe:TimeFrame)->int:
        if step_timeframe == TimeFrame.M:
            return Frequency.MONTH
        elif step_timeframe == TimeFrame.W:
            return  Frequency.WEEK
        elif step_timeframe == TimeFrame.D:
            return  Frequency.DAY
        elif step_timeframe == TimeFrame.H1 or \
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

    def _get_fitted_simulator(self,fitted_data_source: Dict[str, DataFrame])->absTradingSimulator:
        return PyalgotradeTradingSimulator(fitted_data_source, self.__strategy_wrapper_factory,self.__report_storage)