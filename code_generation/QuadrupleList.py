from enum import Enum
from typing import List
from statements.Statement import ArithmeticExpr

class Operation(Enum):
  SUM = 'int'
  DIFF = 'char'
  FLOAT = 'float'
  RETURN = 'return'
  JUMP_F = ''
  JUMP_T = ''

class QuadrupleList:
  quadruples = []
  current_temp = 0

  def get_next_temp(self):
    self.current_temp += 1
    return 't'+str(self.current_temp)

  def add_quadd(self, a, b, c, d):
    self.quadruples.append((a, b, c, d))

  # def add_arithmetic_exp(self, exp: ArithmeticExpr):
  #   self.quadruples.append((exp.op, exp.leftOp, exp.rightOp, self.get_next_temp()))

  # def add_arithmetic_exp(self, exp: ArithmeticExpr):
  #   self.quadruples.append((exp.op, exp.leftOp, exp.rightOp, self.get_next_temp()))



# class CodeGenerator:
#   quad_list = QuadrupleList()
#   op_stack = []
#   jump_stack = []
#   exp_stack = []
#   polish_vec = []

#   def paso1(self,id):
#     polish_vec.push(id)

#   def paso2()
