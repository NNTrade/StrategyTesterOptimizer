from abc import ABC, abstractmethod
from typing import Generic
from typing import Generic, TypeVar

T = TypeVar('T')
class IsValidChecker(ABC, Generic[T]):

    @abstractmethod
    def is_valid(self, validation_object:T)->bool:
        ...

class DefaultChecker(IsValidChecker[T]):
    def is_valid(self, validation_object:T) -> bool:
        return True