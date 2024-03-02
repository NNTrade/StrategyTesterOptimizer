import pprint
from .analyzation_period import AnalyzationPeriod
from ...optimization.config import StrategyConfigSet,OptimizationConfig
from ...common import CandleDataSetConfig
from typing import Dict

class AnalyzationConfig:
    CDS_CFG_F = CandleDataSetConfig.CDS_CFG_F
    PERIOD_F = "period"
    STR_CFG_F = StrategyConfigSet.STR_CFG_F

    def __init__(self,
            candle_data_set_cfg: CandleDataSetConfig,
            analization_period:AnalyzationPeriod,    
            strategy_cfg: StrategyConfigSet = StrategyConfigSet())->None:
        self.__candle_data_set_cfg = candle_data_set_cfg
        self.__analization_period = analization_period
        self.__strategy_cfg = strategy_cfg

    @property
    def candle_data_set_cfg(self)->CandleDataSetConfig:
        return self.__candle_data_set_cfg
    
    @property 
    def period(self)->AnalyzationPeriod:
        return self.__analization_period
    
    @property
    def strategy_cfg(self)->StrategyConfigSet:
        return self.__strategy_cfg
    
    def get_optimization_config_set(self)->OptimizationConfig:
        return OptimizationConfig(self.candle_data_set_cfg,self.period.optimization_period, self.strategy_cfg)

    def to_dict(self) -> Dict:
        return {
            AnalyzationConfig.CDS_CFG_F: self.candle_data_set_cfg,
            AnalyzationConfig.PERIOD_F: self.period,
            AnalyzationConfig.STR_CFG_F: self.strategy_cfg
        }

    def __str__(self):
        return pprint.pformat(self.to_dict(), sort_dicts=False)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((self.candle_data_set_cfg,self.period, self.strategy_cfg))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AnalyzationConfig):
            return False
        return self.to_dict() == other.to_dict()