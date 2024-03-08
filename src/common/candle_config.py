from NNTrade.common import TimeFrame
from typing import Dict, Union
import json

class CandleConfig:
    """Configuration of stock candle. Name of ticker and timeframe of trading data in the one candle
    """
    TICKER_F = "ticker"
    TF_F = "timeframe"

    def __init__(self, ticker: str, timeframe: TimeFrame):
        self.__ticker = ticker
        self.__timeframe = timeframe

    @property
    def ticker(self) -> str:
        """Stock ticker name
        """
        return self.__ticker

    @property
    def timeframe(self) -> TimeFrame:
        """Timeframe in one candle
        """
        return self.__timeframe

    def to_dict(self) -> Dict:
        return {
            CandleConfig.TICKER_F: self.ticker,
            CandleConfig.TF_F: self.__timeframe.short_name() if self.__timeframe is not None else "",
        }

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # Create a hash based on a tuple of hashable attributes
        return hash((self.ticker, self.timeframe))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CandleConfig):
            return False
        return self.to_dict() == other.to_dict()

    def __lt__(self, other):
        # Custom less-than comparison for sorting
        key_order = [
            self.TICKER_F, self.TF_F
        ]
        for key in key_order:
            if getattr(self, key) != getattr(other, key):
                return getattr(self, key) > getattr(other, key)
        return False

    def to_json(self):
        return json.dumps({CandleConfig.TICKER_F: self.ticker, CandleConfig.TF_F: self.__timeframe.short_name()})

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data):
        return cls(data[CandleConfig.TICKER_F], TimeFrame.parse(data[CandleConfig.TF_F]))