from enum import Enum
from typing import List
import pickle

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
  current_param = 0
  pointer = 0

  def get_next_temp(self):
    self.current_temp += 1
    return 't'+str(self.current_temp)

  def get_next_param(self):
    self.current_param += 1
    return 'param'+str(self.current_param)

  def reset_params(self):
    self.current_param = 0

  def add_quadd(self, a, b, c, d):
    self.pointer += 1
    self.quadruples.append((a, b, c, d))

  def update_target(self, dir, a, b, c):
    old_tuple = self.quadruples[dir]
    new_tuple = (old_tuple[0], a or old_tuple[1], b or old_tuple[2], c or old_tuple[3])
    self.quadruples[dir] = new_tuple
