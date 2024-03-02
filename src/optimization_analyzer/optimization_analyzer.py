import logging
import multiprocessing
import pprint
from .config import AnalyzationConfig
from .model import OptimizationAnalyzReport
from ..optimization import absTradingSimulatior, absStrategyFactory, Optimizer, SimulationConfig
from ..optimization.config import OptimizationConfig,List
from .period_splitter import absPeriodSplitter, DefaultPeriodSplitter, AnalyzationPeriod
from ..optimization.strategy.realization import GridStrategyFactory

class OptimizationAnalyzer:
    def __init__(self,
                 simulation_report_factory: absTradingSimulatior, 
                 optimization_strategy_factory: absStrategyFactory = GridStrategyFactory(), 
                 period_splitter: absPeriodSplitter =  DefaultPeriodSplitter.default_tf_d()) -> None:
        self.__optimizer = Optimizer(simulation_report_factory,optimization_strategy_factory)
        self.period_splitter = period_splitter
        self.__logger = logging.getLogger(f"OptimizationAnalyzer")
        pass

    def analys_single_optimization(self, config: AnalyzationConfig)->OptimizationAnalyzReport:
        self.__logger.info(f"Start analisation of:\n{config}")

        self.__logger.info("Begin optimization")
        opt_cfg_set = config.get_optimization_config_set()
        opt_sim_rep = self.__optimizer.optimize(opt_cfg_set)

        self.__logger.info("Get forward report")
        fwd_cfg = SimulationConfig(config.candle_data_set_cfg,config.period.forward_period, opt_sim_rep.simulation_config.strategy_cfg)
        fwd_sim_rep = self.__optimizer.trading_simulator.get_report(fwd_cfg)

        self.__logger.info("Prepare AnalizationReport")
        return OptimizationAnalyzReport(opt_sim_rep, fwd_sim_rep)
    
    def analis_optimization_flow(self, analyzation_config:OptimizationConfig,use_muiltiprocess:bool = False)->List[OptimizationAnalyzReport]:
        self.__logger.info(f"Define analization rounds intervals")
        list_of_analis_periods = self.period_splitter.split(analyzation_config.period)

        # Function to process each period in parallel
        def process_single_optimizaiton(period:AnalyzationPeriod):
            analys_config = AnalyzationConfig(analyzation_config.candle_ds_cfg, period, analyzation_config.strategy_cfg_set)
            self.__logger.info(f"Define AnalyzationConfig for single_optimization:\n{analys_config} ")
            
            analis_report = self.analys_single_optimization(analys_config)
            log_txt = {
                "optimization":{
                    "period":analis_report.optimization.simulation_config.period,
                    "strategy_config": analis_report.optimization.simulation_config.strategy_cfg,
                    "metrics": analis_report.optimization.metrics
                },
                "forward":{
                    "period":analis_report.forward.simulation_config.period,
                    "strategy_config": analis_report.forward.simulation_config.strategy_cfg,
                    "metrics": analis_report.forward.metrics
                }
            }
            self.__logger.info(f"Return analis_report:\n{pprint.pformat(log_txt,sort_dicts=False)}")
            return analis_report
        
        if use_muiltiprocess:
            # Create a pool of worker processes
            with multiprocessing.Pool() as pool:
                # Map the process_period function to each period in the list
                rep_ret = pool.map(process_single_optimizaiton, list_of_analis_periods)
        else:
            rep_ret = [process_single_optimizaiton(analys_period) for analys_period in list_of_analis_periods]
        
        
        return rep_ret


