from .abs_run_report_storage import absRunReportStorage, RunConfig, Union, RunReport


class InMemoryStorage(absRunReportStorage):
  def __init__(self, sub_storage: absRunReportStorage = None) -> None:
    super().__init__(sub_storage)
    self._report_dict = {}

  def _try_get(self, run_config: RunConfig) -> Union[RunReport, None]:
    if run_config in self._report_dict:
      return self._report_dict[run_config]

    return None

  def _try_add(self, run_config: RunConfig, run_report: RunReport) -> bool:
    if run_config in self._report_dict:
      if not run_report == self._report_dict[run_config]:
        raise AttributeError(
            "run config is in storage but with another report")
      return False
    self._report_dict[run_config] = run_report
    return True
