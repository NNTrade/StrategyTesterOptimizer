from typing import Dict


class StrategyId:
  """Id of strategy for define strategy and its version which is using
  """
  NAME_F = "name"
  V_F = "v"

  def __init__(self, name: str, id: str) -> None:
    self.__name = name
    self.__v = id
    pass

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

  def __str__(self):
      return f"{self.name}.{self.version}"

  def __repr__(self):
      return self.__str__()

  def __hash__(self):
      # Create a hash based on a tuple of hashable attributes
      return hash((self.name, self.version))

  def __eq__(self, other: object) -> bool:
      if not isinstance(other, StrategyId):
          return False
      return self.to_dict() == other.to_dict()
