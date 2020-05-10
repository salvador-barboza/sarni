from code_generation.QuadrupleList import QuadrupleList


class SemanticActionHandler:
  quad_list = QuadrupleList()
  jump_stack = []
  last_op = ''

  def consume_arithmetic_op(self, op, a, b):
    temp_var = self.quad_list.get_next_temp()
    self.quad_list.add_quadd(op, a, b, temp_var)
    return temp_var

  def consume_relational_op(self, op, a, b):
    temp_var = self.quad_list.get_next_temp()
    self.quad_list.add_quadd(op, a, b, temp_var)
    return temp_var

  def consume_assignment(self, target, value):
    self.quad_list.add_quadd('=', -1, -1, target)

  def consume_read(self, target):
    self.quad_list.add_quadd('READ', -1, -1, target)

  def consume_write(self, value):
    self.quad_list.add_quadd('WRITE', -1, -1, value)

  def start_if(self):
    self.quad_list.add_quadd('JUMPF', -1, -1, -1)
    self.jump_stack.append(self.quad_list.pointer - 1)

  def end_if(self, cond):
    quad_to_update = self.jump_stack.pop()
    self.quad_list.update_target(quad_to_update, cond, None, self.quad_list.pointer)

  def start_else(self):
    self.quad_list.add_quadd('JUMP', -1, -1, -1)
    self.jump_stack.append(self.quad_list.pointer - 1)

  def end_else(self, cond):
    else_start = self.jump_stack.pop()
    if_start = self.jump_stack.pop()
    self.quad_list.update_target(if_start, cond, None, else_start + 1)
    self.quad_list.update_target(else_start, None, None, self.quad_list.pointer)

  def start_while(self):
    self.jump_stack.append(self.quad_list.pointer - 1)
    self.quad_list.add_quadd('JUMPF', -1, -1, -1)
    self.jump_stack.append(self.quad_list.pointer - 1)

  def end_while(self, cond):
    quad_to_update = self.jump_stack.pop()
    jump_on_false_quad = self.jump_stack.pop()
    self.quad_list.add_quadd('JUMP', -1, -1, jump_on_false_quad)
    self.quad_list.update_target(quad_to_update, cond, None, self.quad_list.pointer)

  def start_do_while(self):
      quad_to_update = self.jump_stack.pop()
      jump_on_false_quad = self.jump_stack.pop()
      self.quad_list.add_quadd('JUMP', -1, -1, jump_on_false_quad)
      self.quad_list.update_target(quad_to_update, self.quad_list.pointer)

  def end_do_while(self):
      quad_to_update = self.jump_stack.pop()
      jump_on_false_quad = self.jump_stack.pop()
      self.quad_list.add_quadd('JUMP', -1, -1, jump_on_false_quad)
      self.quad_list.update_target(quad_to_update, self.quad_list.pointer)