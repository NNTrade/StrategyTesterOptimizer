from src.strategy.run_report import RunReport


def by_strategy_yield_per_year_comparer(prev:RunReport, new: RunReport)->int:
  return int((prev.metrics.capital.strategy_yield_per_year - new.metrics.capital.strategy_yield_per_year)*100000000)