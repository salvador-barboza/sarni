from enum import Enum, auto

"""
Este Enum contiene todas las instrucciones que pueden usarse en nuestro compilador.
Se comparten en el modulo compiler y en vm.
"""
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
  ADD_ADDR = auto()
  ASSIGN = auto()
  PLUS = auto()
  MATR_ADD = auto()
  MINUS = auto()
  MULTIP = auto()
  DIVISION = auto()
  MOD = auto()
  GTR = auto()
  GTR_EQ = auto()
  SMLR = auto()
  SMLR_EQ = auto()
  EQ = auto()
  NOTEQ = auto()
  VER = auto()
  OR = auto()
  AND = auto()

  # Multidim variable instrutions
  MAT_ADD = auto()
  MAT_SUB = auto()
  MAT_MULT = auto()
  MULT_DIM_ASSIGN = auto()
  DETERMINANTE = auto()
  INVERSA = auto()
  TRANSPOSE = auto()


"""
Esta funcion se utiliza para mapear entre un operador y su respectiva operacion para la
maquina virtual.
"""
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
    return Instruction.MOD
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
  elif op == '|':
    return Instruction.OR
  elif op == '&':
    return Instruction.AND