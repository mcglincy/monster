from enum import IntEnum


class ExitKind(IntEnum):
  NO_EXIT = 0
  OPEN = 1
  NEED_KEY = 2
  NEED_NO_KEY = 3
  RANDOM_FAIL = 4
  ACCEPTOR = 5
  NEED_OBJECT = 6
  OPEN_CLOSE = 7
  PASSWORDED = 8