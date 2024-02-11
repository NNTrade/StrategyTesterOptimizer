from ...simulation.models import SimulationReport


def by_strategy_yield_per_year_comparer(prev:SimulationReport, new: SimulationReport)->int:
  return int((new.metrics.capital.strategy_yield_per_year - prev.metrics.capital.strategy_yield_per_year)*100000000)