from dataclasses import dataclass
from enum import Enum

class VarType(Enum):
  INT = 'int'
  CHAR = 'char'
  FLOAT = 'float'

class ReturnType(Enum):
  VOID = 'void'
  INT = 'int'
  CHAR = 'char'
  FLOAT = 'float'

@dataclass
class TuplaTablaVariables:
    name: str
    type: VarType

@dataclass
class TuplaDirectorioFunciones:
    name: str
    return_type: ReturnType
    vars_table: dict

    def add_var(self, tupla: TuplaTablaVariables):
      self.vars_table[tupla.name] = tupla

    def add_vars(self, tuplas: list):
      for t in tuplas:
        self.add_var(t)


class DirectorioFunciones:
  global_var_dir = dict()

  def __init__(self):
    self.dict_funciones = dict()

  def add_func_entry(self, tupla: TuplaDirectorioFunciones):
    # tupla.global_var_dir = global_var_dir
    self.dict_funciones[tupla.name] = tupla

  def add_global_vars(self, tuplas: list):
    for t in tuplas:
      self.vars_table[t.name] = t

