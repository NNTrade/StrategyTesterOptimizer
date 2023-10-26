from ..strategy.absStrategy import absStrategy
from ..strategy.run_config.run_config_set import RunConfigSet


class Tester:
  def __init__(self, strategyFactory: absStrategy.Factory) -> None:
    pass

  def run(self, runConfigSet: RunConfigSet):
    for runCfg in runConfigSet.parameters_as_records
