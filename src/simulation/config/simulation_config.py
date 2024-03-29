from __future__ import annotations
from typing import Dict,List
from .strategy_config import StrategyConfig
from ...common import DatePeriod, CandleConfig, CandleDataSetConfig
import pprint
import json

class SimulationConfig:
    """configuration of single strategy simulation
    """
    CDS_CFG_F = CandleDataSetConfig.CDS_CFG_F
    PERIOD_F = "period"
    STRATEGY_CFG_F = "strategy_cfg"

    def __init__(self, candle_data_set_cfg: CandleDataSetConfig, period: DatePeriod, strategy_cfg: StrategyConfig = StrategyConfig()):
        # Convert to a tuple to make it immutable
        self.__cds_cfg = candle_data_set_cfg
        self.__period = period
        self._strategy_cfg = strategy_cfg

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

    def split(self, chunks_count: int) -> List[SimulationConfig]:        
        return [SimulationConfig(self.candle_ds_cfg, p, self.strategy_cfg) for p in self.period.split(chunks_count)]

    @property
    def strategy_cfg(self) -> StrategyConfig:
        """Strategy configuration parameter
        """
        return self._strategy_cfg

    def to_dict(self) -> Dict:
        return {
            SimulationConfig.CDS_CFG_F: self.candle_ds_cfg,
            SimulationConfig.PERIOD_F: self.period,
            SimulationConfig.STRATEGY_CFG_F: dict(self.strategy_cfg),
        }

    def __str__(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((self.candle_ds_cfg, self.period, self.strategy_cfg))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimulationConfig):
            return False
        return self.to_dict() == other.to_dict()

    def to_json(self):
        return json.dumps({
            SimulationConfig.CDS_CFG_F: self.candle_ds_cfg.to_dict(),
            SimulationConfig.PERIOD_F: self.period.to_dict(True),
            SimulationConfig.STRATEGY_CFG_F: self.strategy_cfg.to_dict()
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        candle_ds_cfg = CandleDataSetConfig.from_dict(data[SimulationConfig.CDS_CFG_F])
        period = DatePeriod.from_dict(data[SimulationConfig.PERIOD_F])
        strategy_cfg = StrategyConfig.from_dict(data[SimulationConfig.STRATEGY_CFG_F])
        return cls(candle_ds_cfg, period, strategy_cfg)