from src import simulation
from .abs_simulation_report_storage import absSimulationReportStorage, SimulationConfig, Union
from ..models import SimulationReport

class InMemoryStorage(absSimulationReportStorage):
  def __init__(self, sub_storage: Union[absSimulationReportStorage,None] = None) -> None:
    super().__init__(sub_storage)
    self._report_dict = {}

  def _try_get(self, simulation_config: SimulationConfig) -> Union[SimulationReport, None]:
    if simulation_config in self._report_dict:
      return self._report_dict[simulation_config]

    return None

  def _try_add(self, simulation_config: SimulationConfig, simulation_report: SimulationReport) -> bool:
    if simulation_config in self._report_dict:
      if not simulation_report == self._report_dict[simulation_config]:
        raise AttributeError(
            "run config is in storage but with another report")
      return False
    self._report_dict[simulation_config] = simulation_report
    return True
