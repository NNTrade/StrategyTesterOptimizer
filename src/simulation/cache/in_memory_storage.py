from .abs_simulation_log_storage import absSimulationLogStorage, SimulationConfig, Union, StrategyId
from ..models import SimulationLog

class InMemoryStorage(absSimulationLogStorage):
  def __init__(self, sub_storage: Union[absSimulationLogStorage,None] = None) -> None:
    super().__init__(sub_storage)
    self._report_dict = {}

  def _try_get(self,  strategy_id:StrategyId, simulation_config: SimulationConfig) -> Union[SimulationLog, None]:
    rep_dic = self._report_dict.get(strategy_id,None)
    if rep_dic is None:
      return None
    
    return rep_dic.get(simulation_config, None)

  def _try_add(self, strategy_id:StrategyId,simulation_config: SimulationConfig, simulation_log: SimulationLog) -> bool:
    
    rep_dic = self._report_dict.get(strategy_id,{})
    exist_log = rep_dic.get(simulation_config, None)
    if exist_log is not None:
      if exist_log != simulation_log:
        raise AttributeError(
            "run config is in storage but with another report")
      return False
    
    rep_dic[simulation_config] = simulation_log
    self._report_dict[strategy_id] = rep_dic
    return True
