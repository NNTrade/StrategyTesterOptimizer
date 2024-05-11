from __future__ import annotations
import logging
from pandas import DataFrame
from ..common.date_period import DatePeriod
from .report.simulation_report import SimulationReport
from .config import SimulationConfig,StrategyId
from .cache.abs_simulation_log_storage import absSimulationLogStorage
from abc import ABC, abstractmethod
from typing import Union, Dict
from .models import SimulationLog

class absTradingSimulator(ABC):
    """Abstract trading simulation factory

    Args:
        ABC (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    def __init__(self, data_source: Dict[str, DataFrame], report_storage: Union[absSimulationLogStorage,None] = None, trading_sim_name:Union[str,None]= None) -> None:
        """Constructor

        Args:
            data_source (Dict[str, DataFrame]): Dictionary with DataFrames mapped by ticker keys
            report_storage (Union[absSimulationLogStorage,None], optional): Storage for cashed reports. Defaults to None.
            trading_sim_name (Union[str,None], optional): Name of simu;lation for logging process. Defaults to None.
        """
        self.__log_cache: Union[absSimulationLogStorage,None] = report_storage
        self.__logger = logging.getLogger(f"absTradingSimulator")
        self._logger = self.__logger if trading_sim_name is None else self.__logger.getChild(trading_sim_name)
        self._data_source = data_source
        pass
    
    @abstractmethod
    def _get_fitted_simulator(self,fitted_data_source: Dict[str, DataFrame])->absTradingSimulator:
        ...

    def get_fitted_simulator(self, date_period:DatePeriod)->absTradingSimulator:
        fitted_data_source = {}
        for ticker, stock_df in self._data_source.items():
            fitted_stock_df = date_period.filter_df(stock_df)
            fitted_data_source[ticker] = fitted_stock_df
        
        simulator = self._get_fitted_simulator(fitted_data_source)
        return simulator
        
    
    @abstractmethod
    def _run(self, strategy_id:StrategyId,run_config: SimulationConfig, alias_data:Dict[str,DataFrame])->SimulationLog:
        """Logic which get result of strategy for run config

        Args:
            run_config (SimulationConfig): run configuration
            alias_data (Dict[str,DataFrame): data of quotes by aliase key

        Returns:
            absRunReportFactory.RunResult: strategy run result
        """
        ...

    def get_log(self, strategy_id:StrategyId, run_config: SimulationConfig, ignore_period:bool = False) -> SimulationLog:
        """get Strategy run report by run configuration

        Args:
            strategy_id (StrategyId): startegy id which must use for run
            run_config (RunConfig): run configuration

        Returns:
            StrategyReport: Strategy run report
        """
        self.__logger.info(f"Getting log of:\n{run_config}")

        if self.__log_cache is not None:
            self.__logger.debug("Try find log in store")
            sl = self.__log_cache.try_get(strategy_id, run_config)
            if sl is not None:
                return sl
        
        self.__logger.debug("Get quotes for simulations")
        alias_data:Dict[str,DataFrame] = {}
        for alias,stock_cfg in run_config.candle_data_set_config.stocks.items():
            df = self._data_source[stock_cfg.ticker]
            if ignore_period:
                alias_data[alias] = df
            else:
                alias_data[alias] = run_config.period.filter_df(df)
        
        self.__logger.debug(f"No cache source or chache not found. Star simulation")
        sl = self._run(strategy_id, run_config,alias_data)

        if self.__log_cache is not None:
          self.__logger.debug("Add log to store")
          self.__log_cache.try_add(strategy_id, run_config,sl)  
        
        if len(sl.deal_list) == 0:
            self.__logger.warning(f"No deals with config: {run_config}")


        return sl
    
    def get_report(self, strategy_id:StrategyId,simulation_config: SimulationConfig, ignore_period:bool = False) -> SimulationReport: 
        self.__logger.info(f"Getting report of\n{simulation_config}")
        sl = self.get_log(strategy_id, simulation_config, ignore_period)

        self.__logger.debug("Convert log into report")
        report = SimulationReport(strategy_id, simulation_config, sl)
        self.__logger.info(f"Simulation report metric:\n{report.metrics}")
        return report