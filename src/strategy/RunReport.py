from __future__ import annotations
from .run_config import RunConfig
from . import Strategy


class RunReport:
  # TODO: [FI-83] Описать RunReport
  """Report of strategy run
  """

  def __init__(self) -> None:
    pass

  class Factory:
    # TODO: [FI-84] Описать RunReport.Factory
    def __init__(self, strategy_factory: Strategy.Factory, report_storage) -> None:
      pass

    def get(self, run_config: RunConfig) -> RunReport:
      """get Strategy run report by run configuration

      Args:
          run_config (RunConfig): run configuration

      Returns:
          StrategyReport: Strategy run report
      """
