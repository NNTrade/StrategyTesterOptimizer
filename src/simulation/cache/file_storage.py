from math import fabs
from .abs_simulation_log_storage import absSimulationLogStorage, SimulationConfig, Union, StrategyId
from ..models import SimulationLog
import os
from typing import Dict
import json

class InMemoryStorage(absSimulationLogStorage):
    def __init__(self, folder_path:str, sub_storage: Union[absSimulationLogStorage,None] = None) -> None:
        super().__init__(sub_storage)
        self.__folder_path = folder_path

    def build_str_folder(self, strategy_id:StrategyId)->str:
        return os.path.join(self.__folder_path, str(strategy_id))
    def _try_get(self,  strategy_id:StrategyId, simulation_config: SimulationConfig) -> Union[SimulationLog, None]:
        
        file_path = self.get_full_path(strategy_id, simulation_config)

        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            loaded_dict = json.load(f)

        
    def parse_dict(self, cur_path:str, parse_dict:Dict)->str:
        sorted_keys = sorted(parse_dict.keys())

        for key in sorted_keys:
            value = parse_dict[key]
            cur_path = os.path.join(cur_path, key)
            if isinstance(value, dict):
                cur_path = self.parse_dict(cur_path, value)
            elif isinstance(value, list) or isinstance(value, tuple):
                cur_path = os.path.join(cur_path, "__".join(value))
            else:
                cur_path = os.path.join(cur_path, value)
        return cur_path

    def get_full_path(self, strategy_id:StrategyId,simulation_config: SimulationConfig)->str:
        str_folder =self.build_str_folder(strategy_id)
        cfg_dict = simulation_config.to_dict()        
        full_path = self.parse_dict(str_folder, cfg_dict)
        return os.path.join(full_path, 'SimulationLog.json')
    def _try_add(self, strategy_id:StrategyId,simulation_config: SimulationConfig, simulation_log: SimulationLog) -> bool:
        file_path = self.get_full_path(strategy_id, simulation_config)
        
        if os.path.exists(file_path):
            return False
        
        simulation_log_dict = simulation_log.to_dict()
        with open(file_path, 'w') as f:
            json.dump(simulation_log_dict, f)   

        return True
