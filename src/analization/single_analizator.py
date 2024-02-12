from .config import AnalizationConfig
from .model import AnalizationReport
from ..optimization import absTradingSimulatior, absFactory, Optimizer, OptimizationConfigSet,SimulationConfig
class Single_Analizator:
    def __init__(self,simulation_report_factory: absTradingSimulatior, optimization_strategy_factory: absFactory ) -> None:
        self.__optimizer = Optimizer(simulation_report_factory,optimization_strategy_factory)
        pass
    
    def analis(self, config: AnalizationConfig)->AnalizationReport:
        opt_cfg_set = config.get_optimization_config_set()
        opt_sim_rep = self.__optimizer.optimize(opt_cfg_set)

        fwd_cfg = SimulationConfig(config.candle_data_set_cfg,config.period.forward_period, opt_sim_rep.simulation_config.strategy_cfg)
        fwd_sim_rep = self.__optimizer.trading_simulator.get_report(fwd_cfg)
        return AnalizationReport(opt_sim_rep, fwd_sim_rep)