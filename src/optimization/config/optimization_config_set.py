from __future__ import annotations
from typing import Generic, List

from ...simulation.config.strategy_config import StrategyConfig
from .strategy_config_sets import T, StrategyConfigSet
from ...simulation.config import SimulationConfig
from ...common import CandleDataSetConfig ,DatePeriod

class OptimizationConfigSet:
    """Run configuration set
    """

    def __init__(self, candle_data_set_cfg: CandleDataSetConfig,period: DatePeriod, strategy_cfg_set: StrategyConfigSet) -> None:
        self.__cds_cfg = candle_data_set_cfg
        self.__period = period
        self.__strategy_cfg_set = strategy_cfg_set
        pass

    @property
    def candle_data_set_config(self) -> CandleDataSetConfig:
        """candle data set config
        """
        return self.__cds_cfg
    
    @property
    def candle_ds_cfg(self) -> CandleDataSetConfig:
        """candle data set config
        """
        return self.__cds_cfg

    @property
    def period(self) -> DatePeriod:
        """using period
        """
        return self.__period    

    def split(self, chunks_count: int) -> List[OptimizationConfigSet]:        
        return [OptimizationConfigSet(self.candle_ds_cfg, p, self.strategy_cfg_set) for p in self.period.split(chunks_count)]

    @property
    def strategy_cfg_set(self) -> StrategyConfigSet:
        """Set of strategy configurations
        """
        return self.__strategy_cfg_set

    def as_records(self) -> List[SimulationConfig]:
        _ret = []
        for s_rec in self.__strategy_cfg_set.as_records():
            _ret.append(SimulationConfig(self.candle_ds_cfg, self.period, s_rec))
        return _ret
    
