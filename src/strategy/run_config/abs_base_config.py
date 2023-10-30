from typing import Callable, Generic, TypeVar, List
from enum import Enum
from abc import ABC, abstractmethod
T = TypeVar('T')
RT = TypeVar('RT')


class absBaseConfigSet(ABC, Generic[T]):
    class record_type(Enum):
        only_valid = 1
        only_invalid = -1
        all = 0

    def __init__(self, is_valid_func: Callable[[T], bool] = None) -> None:
        self.__is_valid_func = is_valid_func if is_valid_func is not None else lambda config: True
        super().__init__()

    def is_valid(self, config: T) -> bool:
        return self.__is_valid_func(config)

    @property
    def is_valid_func(self) -> Callable[[T], bool]:
        return self.__is_valid_func

    @abstractmethod
    def _build_records(self) -> List[T]:
        ...

    def as_records(self, record_type: record_type = record_type.only_valid) -> List[T]:
        recs = self._build_records()
        if record_type == record_type.only_valid:
            return [rec for rec in recs if self.is_valid(rec)]
        elif record_type == record_type.only_invalid:
            return [rec for rec in recs if not self.is_valid(rec)]
        else:
            return recs


class absBaseBuilder(ABC, Generic[RT, T]):
    def __init__(self) -> None:
        self.is_valid_func: Callable[[T], bool] = lambda config: True
        super().__init__()

    def add_is_valid_func(self, is_valid_func: Callable[[T], bool]) -> RT:
        self.is_valid_func = is_valid_func
        return self
