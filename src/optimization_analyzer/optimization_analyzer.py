import logging
import multiprocessing
import pprint
from tqdm import tqdm
from .config import AnalyzationConfig
from .model import OptimizationAnalyzReport
from ..optimization import AbsOptimizer,SimulationReport
from ..optimization.config import OptimizationConfig,List
from .period_splitter import absPeriodSplitter, DefaultPeriodSplitter, AnalyzationPeriod
from ..optimization.strategy.realization import GridStrategyFactory
from ..simulation.config import StrategyId,SimulationConfig

class OptimizationAnalyzer:
    def __init__(self,
                 optimizer: AbsOptimizer,
                 period_splitter: absPeriodSplitter =  DefaultPeriodSplitter.default_tf_d()) -> None:
        self.__optimizer = optimizer
        self.period_splitter = period_splitter
        self.__logger = logging.getLogger(f"OptimizationAnalyzer")
        pass

    def analys_single_optimization(self,  strategy_id:StrategyId,config: AnalyzationConfig)->OptimizationAnalyzReport:
        self.__logger.debug(f"Start analisation of:\n{config}")

        self.__logger.debug("Begin optimization")
        opt_cfg_set = config.get_optimization_config_set()
        opt_sim_cfg, opt_sim_rep = self.__optimizer.optimize(strategy_id, opt_cfg_set)

        self.__logger.debug("Get forward report")
        fwd_cfg = SimulationConfig(config.candle_data_set_cfg,config.period.forward_period, opt_sim_cfg.strategy_cfg)
        fwd_sim_rep = self.__optimizer.trading_simulator.get_report(strategy_id,fwd_cfg)

        self.__logger.debug("Prepare AnalizationReport")
        return OptimizationAnalyzReport(opt_sim_cfg,opt_sim_rep, fwd_sim_rep)
    
    def process_single_optimizaiton(self,strategy_id:StrategyId, analyzation_config:OptimizationConfig, period:AnalyzationPeriod):
        analys_config = AnalyzationConfig(analyzation_config.candle_ds_cfg, period, analyzation_config.strategy_cfg_set)
        self.__logger.info(f"Define AnalyzationConfig for single_optimization:\n{analys_config} ")
        
        analis_report = self.analys_single_optimization(strategy_id,analys_config)
        log_txt = {
            "optimization":{
                "period":analis_report.optimized_config.period,
                "strategy_config": analis_report.optimized_config.strategy_cfg,
                "metrics": [ar.metrics for ar in analis_report.optimization]
            },
            "forward":{
                "period":analis_report.forward.simulation_config.period,
                "strategy_config": analis_report.forward.simulation_config.strategy_cfg,
                "metrics": analis_report.forward.metrics
            }
        }
        self.__logger.info(f"Return analis_report:\n{pprint.pformat(log_txt,sort_dicts=False)}")
        return analis_report

    def analis_optimization_flow(self, strategy_id:StrategyId, analyzation_config:OptimizationConfig,use_muiltiprocess:bool = False)->List[OptimizationAnalyzReport]:
        self.__logger.debug(f"Define analization rounds intervals")
        list_of_analis_periods = self.period_splitter.split(analyzation_config.period)

        if use_muiltiprocess:
            # Create a pool of worker processes
            with multiprocessing.Pool() as pool:
                # Map the process_period function to each period in the list
                rep_ret = pool.map(self.process_single_optimizaiton, strategy_id, analyzation_config, list_of_analis_periods)
        else:
            rep_ret = []
            for analys_period in tqdm(list_of_analis_periods):
                rep_ret.append(self.process_single_optimizaiton(strategy_id, analyzation_config,analys_period))
             
        return rep_ret


