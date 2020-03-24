from enum import IntEnum


class Direction(IntEnum):
  INVALID = -1
  NORTH = 0
  SOUTH = 1
  EAST = 2
  WEST = 3
  UP = 4
  DOWN = 5

  @classmethod
  def from_string(cls, name):
    lower_name = name.lower()
    for dir in Direction:
      if dir.name.lower().startswith(lower_name):
        return dir
    return Direction.INVALID

  def opposite(self):
    if self == Direction.NORTH:
      return Direction.SOUTH
    elif self == Direction.SOUTH:
      return Direction.NORTH
    elif self == Direction.EAST:
      return Direction.WEST
    elif self == Direction.WEST:
      return Direction.EAST
    elif self == Direction.UP:
      return Direction.DOWN
    elif self == Direction.DOWN:
      return Direction.UP
    return Direction.INVALID