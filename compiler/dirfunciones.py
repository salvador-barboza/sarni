from dataclasses import dataclass
from enum import Enum

class VarType(Enum):
  INT = 'int'
  CHAR = 'char'
  FLOAT = 'float'
  BOOL = 'bool'

class ReturnType(Enum):
  VOID = 'void'
  INT = 'int'
  CHAR = 'char'
  FLOAT = 'float'

@dataclass
class TuplaTablaVariables:
    name: str
    type: VarType
    addr: int
    dims: (int, int) = (None, None)

@dataclass
class TuplaDirectorioFunciones:
    name: str
    return_type: ReturnType
    param_table: list
    param_pointers: list
    local_variable_count: int
    start_pointer: int
