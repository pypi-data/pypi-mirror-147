from enum import IntEnum, unique

@unique
class ExitStatus(IntEnum):

    SUCCESS = 0
    ERROR = 1
    ERROR_TIMEOUT = 2
    ERROR_CTRL_C = 130
    