from __future__ import annotations
from typing import Dict
from datetime import date
from ..strategy.run_report import Report
from ..strategy.run_config import RunConfigSet


class ParameterSetReport:
    class Key:
        def __init__(self, stock: str, from_date: date, till_date: date, parameters: Dict) -> None:
            self._stock = stock
            self._from_date = from_date
            self._till_date = till_date
            self._parameters = parameters
            self.__hash = hash(
                (self.stock, self.from_date, self.till_date, frozenset(self.parameters.items())))

        @property
        def stock(self):
            return self._stock

        @property
        def from_date(self):
            return self._from_date

        @property
        def till_date(self):
            return self._till_date

        @property
        def parameters(self):
            return self._parameters

        def __eq__(self, other):
            if not isinstance(other, ParameterSetReport.Key):
                return False
            return (self.stock, self.from_date, self.till_date, self.parameters) == (other.stock, other.from_date, other.till_date, other.parameters)

        def __hash__(self):
            return self.__hash

    class Metrics:
        def __init__(self, net_profit: float, max_loss: float, income_deal_vs_loss_deal_rel: float) -> None:
            pass

    def __init__(self, key: ParameterSetReport.Key, metric: ParameterSetReport.Metrics) -> None:
        pass


class TesterReport:
    """Report of testing stage
    """

    class Factory:
        """Factory of Testing stage report
        """

        def __init__(self, strategy_report_factory: Report.Factory) -> None:
            self.__srf = strategy_report_factory
            pass

        def run(self, run_config_set: RunConfigSet) -> TesterReport:
            """Run testing stage, producing Tester stage report

            Args:
                run_config_set (RunConfigSet): _description_

            Returns:
                TesterReport: _description_
            """
            trb = TesterReport.Builder()
            for rec in run_config_set.records:
                srr: Report = self.__srf.get(rec)
                trb.add(srr)

            return trb.build()

    class Builder:
        """Builder of single tester stage report
        """

        def __init__(self):
            pass

        def add(self, strategy_run_report: Report):
            """Add strategy run report to testing stage report

            Args:
                strategy_run_report (StrategyRunReport): _description_
            """
            pass

        def build(self) -> TesterReport:
            """Build testing stage report

            Returns:
                TesterReport: _description_
            """
            return None

    @property
    def records(self) -> Dict[ParameterSetReport.Key, ParameterSetReport.Metrics]:
        return None
