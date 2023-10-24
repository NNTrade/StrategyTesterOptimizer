from ..run_config import RunConfig
from .report import Report
from abc import ABC
from typing import Union


class Storage(ABC):
    """Run report storage client

    Args:
        ABC (_type_): _description_
    """

    def __init__(self) -> None:
        pass

    # BUG [FI-87]: try_get method must recive info about strategy and version for searching reports
    def try_get(self, run_config: RunConfig) -> Union[Report, None]:
        """Search does report for run config exist in storage

        Args:
            run_config (RunConfig): Run config

        Returns:
            Union[Report, None]: Finded report or None if not found
        """
        ...
