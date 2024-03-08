from math import fabs
from .abs_simulation_log_storage import absSimulationLogStorage, SimulationConfig, Union, StrategyId
from ..models import SimulationLog
import os
from typing import Dict
import json
import uuid

class FileStorageCache(absSimulationLogStorage):
    def __init__(self, folder_path:str, sub_storage: Union[absSimulationLogStorage,None] = None) -> None:
        super().__init__(sub_storage)
        self.__folder_path = folder_path
        self.__str_sim_cfg_dict: Dict[StrategyId, Dict[SimulationConfig, str]] = {}
        self.refresh_config_list()

    def refresh_config_list(self):
        self.__str_sim_cfg_dict = {}
        for str_folder in os.listdir(self.__folder_path):
            str_id = StrategyId.from_str(str_folder)
            sim_cfg_dict = self.__str_sim_cfg_dict.get(str_id,{})
            str_folder_path = self._config_folder(str_id)
            
            for filename in os.listdir(str_folder_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(str_folder_path, filename)
                    with open(file_path, "r") as file:
                        # Load JSON from file
                        json_str = file.read()
                        # Convert JSON string to MyClass instance
                        sim_cfg = SimulationConfig.from_json(json_str)
                        # Now you can work with the MyClass instance
                        sim_cfg_dict[sim_cfg] = filename
            self.__str_sim_cfg_dict[str_id] = sim_cfg_dict

    def _build_str_folder(self, strategy_id:StrategyId)->str:
        return os.path.join(self.__folder_path, str(strategy_id))

    def _config_folder(self, strategy_id:StrategyId)->str:
        str_folder = self._build_str_folder(strategy_id)
        return os.path.join(str_folder,"configs")
    
    def _logs_folder(self, strategy_id:StrategyId)->str:
        str_folder = self._build_str_folder(strategy_id)
        return os.path.join(str_folder,"logs")
    
    def _load_log(self, strategy_id:StrategyId, log_id:str)->SimulationLog:
        logs_path = self._logs_folder(strategy_id)
        log_path = os.path.join(logs_path, log_id)
        with open(log_path, "r") as file:
            json_str = file.read()
            return SimulationLog.from_json(json_str)
        
    def _try_get(self,  strategy_id:StrategyId, simulation_config: SimulationConfig) -> Union[SimulationLog, None]:
        sim_cfg_dict = self.__str_sim_cfg_dict.get(strategy_id,{})

        if len(sim_cfg_dict) == 0:
            return None

        sim_id =  sim_cfg_dict.get(simulation_config,None)
        if sim_id is None:
            return None
        
        return self._load_log(strategy_id, sim_id)

    def _try_add(self, strategy_id:StrategyId,simulation_config: SimulationConfig, simulation_log: SimulationLog) -> bool:
        sim_cfg_dict = self.__str_sim_cfg_dict.get(strategy_id,{})

        sim_id = sim_cfg_dict.get(simulation_config,None)
        if sim_id is not None:
            return False
        
        logs_path = self._logs_folder(strategy_id)
        os.makedirs(logs_path, exist_ok=True)
        configs_path = self._config_folder(strategy_id)
        os.makedirs(configs_path, exist_ok=True)

        new_guid = uuid.uuid4()
        file_name = f"{new_guid}.json"

        log_path = os.path.join(logs_path, file_name)
        config_path = os.path.join(configs_path, file_name)

        with open(log_path, "w") as json_file:
            json_file.write(simulation_log.to_json())

        with open(config_path, "w") as json_file:
            json_file.write(simulation_config.to_json())

        sim_cfg_dict[simulation_config] = file_name
        self.__str_sim_cfg_dict[strategy_id] = sim_cfg_dict
        return True
