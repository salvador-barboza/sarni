from enum import Enum, auto

class Instruction(Enum):
  JUMP = auto()
  JUMPF = auto()
  ERA = auto()
  PARAM = auto()
  RETURN = auto()
  ENDFUN = auto()
  GOSUB = auto()
  WRITE = auto()
  READ = auto()
  ASSIGN = auto()
  PLUS = auto()
  MINUS = auto()
  MULTIP = auto()
  DIVISION = auto()
  MODULE = auto()
  GTR = auto()
  GTR_EQ = auto()
  SMLR = auto()
  SMLR_EQ = auto()
  EQ = auto()
  NOTEQ = auto()

def get_instr_for_op(op):
  if op == '+':
    return Instruction.PLUS
  elif op == '-':
    return Instruction.MINUS
  elif op == '*':
    return Instruction.MULTIP
  elif op == '/':
    return Instruction.DIVISION
  elif op == '%':
    return Instruction.MODULE
  elif op == '<':
    return Instruction.SMLR
  elif op == '<=':
    return Instruction.SMLR_EQ
  elif op == '>':
    return Instruction.GTR
  elif op == '>=':
    return Instruction.GTR_EQ
  elif op == '==':
    return Instruction.EQ
  elif op == '!=':
    return Instruction.NOTEQ