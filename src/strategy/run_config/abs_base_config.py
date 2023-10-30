from typing import Callable, Generic, TypeVar

T = TypeVar('T')
RT = TypeVar('RT')


class absBaseConfigSet(Generic[T]):

  def __init__(self, is_valid_func: Callable[[T], bool] = None) -> None:
    self.__is_valid_func = is_valid_func if is_valid_func is not None else lambda config: True
    super().__init__()

  def is_valid(self, config: T) -> bool:
    return self.__is_valid_func(config)

  @property
  def is_valid_func(self) -> Callable[[T], bool]:
      return self.__is_valid_func


class absBaseBuilder(Generic[RT, T]):
   def __init__(self) -> None:
     self.is_valid_func: Callable[[T], bool] = lambda config: True
     super().__init__()

   def add_is_valid_func(self, is_valid_func: Callable[[T], bool]) -> RT:
      self.is_valid_func = is_valid_func
      return self
