from .optimization_market_set_config import OptimizationMarketSetConfig
from ...strategy.run_config import Callable, MarketConfig, RunConfig, StrategyConfigSet, StrategyId,Dict


class OptimizatianConfig:
  STRATEGY_ID_F = RunConfig.STRATEGY_ID_F
  OPT_MARKET_SET_CFG_F = "opt_market_set_cfg"
  STRATEGY_CFG_F = RunConfig.STRATEGY_CFG_F
  def __init__(self, strategy_id: StrategyId, optimization_market_config: OptimizationMarketSetConfig, strategy_cfg: StrategyConfigSet = StrategyConfigSet(), is_valid_func: Callable[[RunConfig], bool] = None):
    # Convert to a tuple to make it immutable
    self._strategy_id = strategy_id
    self._opt_market_set_cfg = optimization_market_config
    self._strategy_cfg = strategy_cfg
  
  @property
  def strategy_id(self)->StrategyId:
    return self._strategy_id
  
  @property
  def optimization_market_set_cfg(self)->OptimizationMarketSetConfig:
    return self._opt_market_set_cfg
  
  @property
  def strategy_cfg(self)->StrategyConfigSet:
    return self._strategy_cfg
  
  def to_dict(self) -> Dict:
      return {
          OptimizatianConfig.STRATEGY_ID_F: self.strategy_id.to_dict(),
          OptimizatianConfig.OPT_MARKET_SET_CFG_F: self.optimization_market_set_cfg.to_dict(),
          OptimizatianConfig.STRATEGY_CFG_F: dict(self.strategy_cfg)
      } 

  def __str__(self):
      return f"{self.to_dict()}"

  def __repr__(self):
      return self.__str__()

  def __hash__(self):
      # Create a hash based on a tuple of hashable attributes
      return hash((self.strategy_id, self.optimization_market_set_cfg, self.strategy_cfg))

  def __eq__(self, other: object) -> bool:
      if not isinstance(other, OptimizatianConfig):
          return False
      return self.to_dict() == other.to_dict()