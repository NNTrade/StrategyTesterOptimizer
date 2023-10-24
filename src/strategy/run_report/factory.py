from .. import Strategy
from ..run_config import RunConfig
from .report import Report
from .storage import Storage


class Factory:
    """Factory for producing Reports of strategy run by RunConfig
    """

    def __init__(self, strategy_factory: Strategy.Factory, report_storage: Storage = None) -> None:
        """Constructor

        Args:
            strategy_factory (Strategy.Factory): Strategy factory
            report_storage (Storage, optional): Run report storage. Defaults to None.
        """
        self.__strategy_factory: Strategy.Factory = strategy_factory
        self.__report_storage: Storage = report_storage
        pass

    def get(self, run_config: RunConfig) -> Report:
        """get Strategy run report by run configuration

        Args:
            run_config (RunConfig): run configuration

        Returns:
            StrategyReport: Strategy run report
        """
        if self.__report_storage is not None:
            rr = self.__report_storage.try_get(run_config)
            if rr is not None:
                return rr

        strategy = self.__strategy_factory.build(run_config.parameters)
        strategy.run(run_config.stock_list,
                     run_config.from_date, run_config.till_date)

        return Report(strategy)
