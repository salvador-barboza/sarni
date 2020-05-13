from code_generation.QuadrupleList import QuadrupleList
from cubosemantico import CuboSemantico
from dirfunciones import TuplaTablaVariables, DirectorioFunciones, VarType

class SemanticActionHandler:
  quad_list = QuadrupleList()
  jump_stack = []
  last_op = ''
  cubo_seman = CuboSemantico()
  global_var_table = dict()
  current_local_var_table: dict()

  def resolve_primitive_type(self, s):
    if (type(s) == int):
      return 'int'
    elif(type(s) == float):
      return 'float'
    else:
      var = self.current_local_var_table.get(s)
      if (var == None):
        raise Exception('variable {} was not declared in the current scope'.format(s))
      else:
        return var.type.value

  #estatutos
  def consume_arithmetic_op(self, op, a, b):
      primitive_a = self.resolve_primitive_type(a)
      primitive_b = self.resolve_primitive_type(b)
      result_type = self.cubo_seman.typematch(primitive_a, op, primitive_b)

      if (result_type == "error"):
        raise Exception('TYPE MISMATCH. {}({}) and {}({}) should be compatible through {} operation'.format(str(a),primitive_a,str(b),primitive_b,str(op)))

      temp_var = self.quad_list.get_next_temp()
      self.quad_list.add_quadd(op, a, b, temp_var)
      self.current_local_var_table[temp_var] = TuplaTablaVariables(name=temp_var, type=VarType(result_type))
      return temp_var

  def consume_relational_op(self, op, a, b):
    primitive_a = self.resolve_primitive_type(a)
    primitive_b = self.resolve_primitive_type(b)
    result_type = self.cubo_seman.typematch(primitive_a, op, primitive_b)
    print(primitive_a)
    print(primitive_b)
    print(result_type)

    if (result_type == "error"):
      raise Exception('TYPE MISMATCH. {}({}) and {}({}) should be compatible through {} operation'.format(str(a),primitive_a,str(b),primitive_b,str(op)))
    
    temp_var = self.quad_list.get_next_temp()
    self.quad_list.add_quadd(op, a, b, temp_var)
    return temp_var

  def consume_assignment(self, target, value):
    primitive_target = self.resolve_primitive_type(target)
    primitive_value = self.resolve_primitive_type(value)

    if (primitive_target != primitive_value):
      raise Exception('TYPE MISMATCH. {} can\'t be assigned to {}'.format(primitive_value, primitive_target))

    self.quad_list.add_quadd('=', value, -1, target)

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

  def start_for(self):
    self.jump_stack.append(self.quad_list.pointer - 2)
    self.jump_stack.append(self.quad_list.pointer - 1)
    self.quad_list.add_quadd('JUMPF', -1, -1, -1)
    self.jump_stack.append(self.quad_list.pointer - 1)

  def end_for(self, cond):
    quad_to_update = self.jump_stack.pop()
    jump_on_false_quad = self.jump_stack.pop()
    quad_declared = self.jump_stack.pop()
    self.quad_list.add_quadd('+', 1, -1, self.quad_list.quadruples[quad_declared][3])
    self.quad_list.add_quadd('JUMP', -1, -1, jump_on_false_quad)
    self.quad_list.update_target(quad_to_update, cond, None, self.quad_list.pointer)

  # Variables y funciones
  def start_global_var_declaration(self):
    self.current_local_var_table = self.global_var_table

  def start_func_scope_var_declaration(self, scope):
    self.current_local_var_table = dict()

  def add_variable_to_current_scope(self, var: TuplaTablaVariables):
    self.current_local_var_table[var.name] = var
