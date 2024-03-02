from __future__ import annotations
import pprint
from typing import Dict,List
from NNTrade.common import TimeFrame
from .candle_config import CandleConfig

class CandleDataSetConfig:
    """Configuration of stock candle data set.
    """
    CDS_CFG_F = "candle_data_set"
    STOCKS_F = "stocks"
    STEP_TF_F = "step_timeframe"

    @staticmethod
    def BuildFromDict(stocks: Dict[str,CandleConfig], step_timeframe: TimeFrame) -> CandleDataSetConfig:
        return CandleDataSetConfig(stocks, step_timeframe)
    
    @staticmethod
    def BuildFromList(stocks: List[CandleConfig], step_timeframe: TimeFrame) -> CandleDataSetConfig:
        return CandleDataSetConfig({f"{i}":sc for i, sc in enumerate(stocks)}, step_timeframe)
    
    @staticmethod
    def BuildFrom(stock: CandleConfig, step_timeframe: TimeFrame, alise_name:str="default") -> CandleDataSetConfig:
        return CandleDataSetConfig({alise_name:stock}, step_timeframe)
    
    def __init__(self, stocks: Dict[str,CandleConfig], step_timeframe: TimeFrame):
        if len(stocks) < 1:
            raise AttributeError(
                "You must set at least one stock", name="stocks")
        for key, stock in stocks.items():
            if stock.timeframe is not None:
                if stock.timeframe < step_timeframe:
                    raise AttributeError("Timeframe of ticker must be LT step timeframe",
                                        name="step_timeframe", obj=step_timeframe)
        self.__stocks = stocks.copy()
        self.__step_timeframe = step_timeframe

    @property
    def stocks(self) -> Dict[str,CandleConfig]:
        """Dictionary alias in strategy and Stock config for this alias in strategy
        """
        return self.__stocks.copy()

    @property
    def step_timeframe(self) -> TimeFrame:
        """Timeframe shift in one row. If step_timeframe < stocks.timeframe than several rows in dataset represent changing of one candle in time
        """
        return self.__step_timeframe
                                 
    def to_dict(self) -> Dict:
        return {
            CandleDataSetConfig.STOCKS_F: {k:s.to_dict() for k,s in self.__stocks.items()},
            CandleDataSetConfig.STEP_TF_F: self.step_timeframe.short_name()
        }

    def __str__(self):
        return  pprint.pformat(self.to_dict(), sort_dicts=False)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((frozenset(self.__stocks.items()), self.step_timeframe))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CandleDataSetConfig):
            return False
        return self.to_dict() == other.to_dict()