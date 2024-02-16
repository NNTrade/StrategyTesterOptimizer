from ..abs_report_comparer import absReportComparer,SimulationReport


class ByYieldPerYear(absReportComparer):
    def __init__(self) -> None:
        self.__mult = 100000000
        super().__init__("ByYieldPerYear")

    def comparer(self,prev:SimulationReport, new: SimulationReport)->int:
        compare_result = int((new.metrics.capital.strategy_yield_per_year - prev.metrics.capital.strategy_yield_per_year)*self.__mult)
        if compare_result > 0:
            self._logger.info(f"New result {new.metrics.capital.strategy_yield_per_year} > {prev.metrics.capital.strategy_yield_per_year}. Compare result {compare_result/self.__mult}")
        else:
            self._logger.info(f"New result {new.metrics.capital.strategy_yield_per_year} < {prev.metrics.capital.strategy_yield_per_year}. Compare result {compare_result/self.__mult}")
        return compare_result
        
