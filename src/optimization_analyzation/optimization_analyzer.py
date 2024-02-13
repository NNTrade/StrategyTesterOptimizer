import logging
import multiprocessing

from .config import AnalyzationConfig
from .model import AnalyzationReport
from ..optimization import absTradingSimulatior, absFactory, Optimizer, SimulationConfig
from ..optimization.config import OptimizationConfig,List
from .period_splitter import absPeriodSplitter, DefaultPeriodSplitter, AnalyzationPeriod

class OptimizationAnalyzer:
    def __init__(self,
                 simulation_report_factory: absTradingSimulatior, 
                 optimization_strategy_factory: absFactory, 
                 period_splitter: absPeriodSplitter =  DefaultPeriodSplitter.default_tf_d()) -> None:
        self.__optimizer = Optimizer(simulation_report_factory,optimization_strategy_factory)
        self.period_splitter = period_splitter
        self.__logger = logging.getLogger(f"SingleAnalizator")
        pass

    def analys_single_optimization(self, config: AnalyzationConfig)->AnalyzationReport:
        self.__logger.info(f"Start analisation of {config}")

        self.__logger.info("Begin optimization")
        opt_cfg_set = config.get_optimization_config_set()
        opt_sim_rep = self.__optimizer.optimize(opt_cfg_set)

        self.__logger.info("Get forward report")
        fwd_cfg = SimulationConfig(config.candle_data_set_cfg,config.period.forward_period, opt_sim_rep.simulation_config.strategy_cfg)
        fwd_sim_rep = self.__optimizer.trading_simulator.get_report(fwd_cfg)

        self.__logger.info("Prepare AnalizationReport")
        return AnalyzationReport(opt_sim_rep, fwd_sim_rep)
    
    def analis_optimization_flow(self, analyzation_config:OptimizationConfig,use_muiltiprocess:bool = True)->List[AnalyzationReport]:
        self.__logger.info(f"Define analization rounds intervals")
        list_of_analis_periods = self.period_splitter.split(analyzation_config.period)

        # Function to process each period in parallel
        def process_single_optimizaiton(period:AnalyzationPeriod):
            analys_config = AnalyzationConfig(analyzation_config.candle_ds_cfg, period, analyzation_config.strategy_cfg_set)
            return self.analys_single_optimization(analys_config)
        
        if use_muiltiprocess:
            # Create a pool of worker processes
            with multiprocessing.Pool() as pool:
                # Map the process_period function to each period in the list
                rep_ret = pool.map(process_single_optimizaiton, list_of_analis_periods)
        else:
            rep_ret = [process_single_optimizaiton(analys_period) for analys_period in list_of_analis_periods]
        
        
        return rep_ret


