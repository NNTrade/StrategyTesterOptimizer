from ..abs_optimizer import AbsOptimizer, absTradingSimulatior, absStrategyFactory, StrategyId, OptimizationConfig, SimulationReport,Tuple
from typing import List
import numpy as np
from datetime import timedelta
from ....common import DatePeriod
from ....simulation.config import SimulationConfig


class SimpleOptimizer(AbsOptimizer):
    def __init__(self, trading_simulator: absTradingSimulatior, optimization_strategy_factory: absStrategyFactory | None = None) -> None:
        super().__init__(SimpleOptimizer, trading_simulator, optimization_strategy_factory)
        pass

    def optimize(self, strategy_id: StrategyId, optimization_config_set: OptimizationConfig) -> Tuple[SimulationConfig,List[SimulationReport]]:
        self.__logger.info("Start optimization")

        # Get new parameter optimizator of current optimization perido
        pof = self._parametar_optimizator_factory.build(
            optimization_config_set.strategy_cfg_set)

        sc = pof.first()
        while sc is not None:
            sc = SimulationConfig(
                optimization_config_set.candle_ds_cfg, optimization_config_set.period, sc)
            sr = self.trading_simulator.get_report(strategy_id, sc)
            sc = pof.next([sr])

        best_opt_sr = pof.best()

        if best_opt_sr is None:
            raise Exception("No simulation report has been found")
        
        return SimulationConfig(optimization_config_set.candle_ds_cfg, optimization_config_set.period, best_opt_sr[0]), best_opt_sr[1]
