from __future__ import annotations
from typing import Dict
import re

class StrategyId:
  """Id of strategy for define strategy and its version which is using
  """
  NAME_F = "name"
  V_F = "v"

  def __init__(self, name: str, id: str) -> None:
    assert not self.__contains_invalid_symbols(name), "Strategy name contain invalid symbol"
    assert not self.__contains_invalid_symbols(id), "Strategy id contain invalid symbol"
    self.__name = name
    self.__v = id
    pass
  def __contains_invalid_symbols(self, s:str)->bool:
    # Define the pattern to match the invalid symbols
    return "[" in s or "]" in s
  @property
  def name(self) -> str:
      """Name of strategy

      Returns:
          str: Name
      """
      return self.__name

  @property
  def version(self) -> str:
      """Version of strategy

      Returns:
          str: Version
      """
      return self.__v

  def to_dict(self) -> Dict:
      return {
          StrategyId.NAME_F: self.name,
          StrategyId.V_F: self.version,
      }

  @classmethod
  def from_str(cls, name:str)->StrategyId:
      splitted_arr = name.split("[")
      str_name, version = splitted_arr[0], splitted_arr[1][:-1]
      return cls(str_name,version)

  def __str__(self):
      return f"{self.name}[{self.version}]"

  def __repr__(self):
      return self.__str__()

  def __hash__(self):
      # Create a hash based on a tuple of hashable attributes
      return hash((self.name, self.version))

  def __eq__(self, other: object) -> bool:
      if not isinstance(other, StrategyId):
          return False
      return self.to_dict() == other.to_dict()
