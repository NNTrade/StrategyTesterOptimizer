from re import S
from ..abs_optimizer import AbsOptimizer, absTradingSimulator, absStrategyFactory, StrategyId, OptimizationConfig, SimulationReport, Tuple
from typing import List
import numpy as np
from datetime import timedelta
from ....common import DatePeriod
from ....simulation.config import SimulationConfig


class ComplexOptimizer(AbsOptimizer):
    """Complex Optimizer. Split given period on set of periods, seach parameters which give best result in periods set

    Args:
        AbsOptimizer (_type_): _description_
    """
    def __init__(self, trading_simulator: absTradingSimulator, optimization_strategy_factory: absStrategyFactory | None = None, proportions: List[int] = [1, 1, 1]) -> None:
        super().__init__(ComplexOptimizer, trading_simulator, optimization_strategy_factory)
        self.__proportions: List[int] = proportions
        pass

    def _split_period(self, period: DatePeriod) -> List[DatePeriod]:
        total_proportion = np.sum(self.__proportions)

        days_in_one = period.period_in_days / total_proportion
        ret_periods: List[DatePeriod] = []
        last_untill_date = period.from_date

        for proportion in self.__proportions:
            proportion_days = days_in_one * proportion
            untill_date = last_untill_date + timedelta(days=proportion_days)

            if untill_date > period.untill_date:
                untill_date = period.untill_date

            ret_periods.append(DatePeriod(last_untill_date, untill_date))

            if untill_date == period.untill_date:
                break
            
            last_untill_date = untill_date

        assert len(ret_periods) == len(
            self.__proportions), "Cann't make same amount of proportion as needed"

        return ret_periods

    def optimize(self, strategy_id: StrategyId, optimization_config_set: OptimizationConfig) -> Tuple[SimulationConfig, List[SimulationReport]]:
        self._logger.info("Start optimization")

        periods = self._split_period(optimization_config_set.period)
        period_trade_sims = {period: self.trading_simulator.get_fitted_simulator(period) for period in periods}

        # Get new parameter optimizator of current optimization perido
        pof = self._parametar_optimizator_factory.build(
            optimization_config_set.strategy_cfg_set)

        sc = pof.first()
        while sc is not None:
            sim_reports = []
            for period,trade_sim in period_trade_sims.items():
                sim_cfg = SimulationConfig(
                    optimization_config_set.candle_ds_cfg, period, sc)
                sim_rep = trade_sim.get_report(strategy_id, sim_cfg, True)
                sim_reports.append(sim_rep)

            sc = pof.next(sim_reports)

        best_opt_sr = pof.best()

        if best_opt_sr is None:
            raise Exception("No simulation report has been found")

        return SimulationConfig(optimization_config_set.candle_ds_cfg, optimization_config_set.period, best_opt_sr[0]), best_opt_sr[1]
