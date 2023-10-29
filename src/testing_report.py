from __future__ import annotations
from typing import Dict, List
from datetime import date
from .strategy.run_report import RunReport
from .strategy.run_config.run_config_set import RunConfigSet
from .strategy.run_report import RunReportFactory


class TestingReport:
    """Report of testing stage
    """

    class Factory:
        def __init__(self, runReportFactory: RunReportFactory) -> None:
            self.__run_report_factory = runReportFactory
            pass

        def get(self, runConfigSet: RunConfigSet) -> TestingReport:
            trb = TestingReport.Builder()
            for rc in runConfigSet.as_records():
                rr = self.__run_report_factory.get(rc)
                trb.add(rr)
            return trb.build()

    class Builder:
        """Builder of single tester stage report
        """

        def __init__(self):
            self.run_report_list = []
            pass

        def add(self, strategy_run_report: RunReport):
            """Add strategy run report to testing stage report

            Args:
                strategy_run_report (StrategyRunReport): _description_
            """
            self.run_report_list.append(strategy_run_report)
            pass

        def build(self) -> TestingReport:
            """Build testing stage report

            Returns:
                TesterReport: _description_
            """
            return TestingReport(self.run_report_list)

    def __init__(self, run_report_list: List[RunReport]) -> None:
        self.__run_report_list = run_report_list.copy()
        pass

    @property
    def run_report_list(self) -> List[RunReport]:
        return self.__run_report_list.copy()
