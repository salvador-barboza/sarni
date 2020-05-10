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
  pointer = 0

  def get_next_temp(self):
    self.current_temp += 1
    return 't'+str(self.current_temp)

  def add_quadd(self, a, b, c, d):
    self.pointer += 1
    self.quadruples.append((a, b, c, d))

  def update_quad_target(self, dir, value):
    old_tuple = self.quadruples[dir]
    new_tuple = (old_tuple[0], old_tuple[1], old_tuple[2], value)
    self.quadruples[dir] = new_tuple

