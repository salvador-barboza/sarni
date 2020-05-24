from compiler.quadruplelist import QuadrupleList
from compiler.cubosemantico import CuboSemantico
from compiler.dirfunciones import TuplaTablaVariables, VarType, TuplaDirectorioFunciones
from compiler.memory import VirtualMemoryManager
from shared.instruction_set import Instruction, get_instr_for_op

class SemanticActionHandler:
  quad_list = QuadrupleList()
  jump_stack = []
  last_op = ''
  cubo_seman = CuboSemantico()
  global_var_table = dict()
  current_local_var_table: dict()
  current_scope = 'global'
  param_table = dict()
  constant_map = dict()
  virtual_memory_manager = VirtualMemoryManager()

  def resolve_var(self, v):
      var_name = v
      is_array = type(v) == tuple
      if is_array:
        var_name = v[0]

      var = self.global_var_table.get(var_name)
      if (var == None):
        var = self.current_local_var_table.get(var_name)
      elif (var == None):
        var = self.current_local_var_table.get(var_name)

      return var

  def resolve_primitive_type(self, s):
    var_id = s
    if (type(s) == tuple):
      var_id = s[0]

    if (type(var_id) == int):
      return 'int'
    elif(type(var_id) == float):
      return 'float'
    else:
      var_type = self.resolve_var(var_id)
      if (var_type != None):
        return var_type.type.value

  def get_addr(self, type, scope):
    if scope == 'global':
      return self.virtual_memory_manager.global_addr.next(type)
    else:
      return self.virtual_memory_manager.local_addr.next(type)

  def allocate_block(self, type, scope, size):
    if scope == 'global':
      return self.virtual_memory_manager.global_addr.allocate_block(type, size)
    else:
      return self.virtual_memory_manager.local_addr.allocate_block(type, size)

  def get_temp_addr(self, type):
    return self.virtual_memory_manager.temp_addr.next(type)

  def resolve_address(self, s):
    var = self.resolve_var(s)
    is_array = type(s) == tuple and s[1] != None and s[2] != None
    if var != None:
      if is_array:
        addr = var.addr
        if var.dims[1] > 0:
          addr += self.resolve_address(s[1]) * var.dims[0]
          addr += self.resolve_address(s[2])
        else:
          addr += self.resolve_address(s[1])

        return addr
      else:
        return var.addr
    else:
      return self.get_or_create_constant_addr(s)

  def get_or_create_constant_addr(self, c):
    addr = self.constant_map.get(c)
    if addr == None:
      var_type = VarType(type(c).__name__)
      addr = self.virtual_memory_manager.const_addr.next(var_type)
      self.constant_map[c] = addr

    return addr

  def validate_operation_and_get_result_type(self, op, a, b):
      primitive_a = self.resolve_primitive_type(a)
      primitive_b = self.resolve_primitive_type(b)

      if (primitive_a == None):
        raise Exception('variable {} was not declared in the current scope'.format(a))

      if (primitive_b == None):
        raise Exception('variable {} was not declared in the current scope'.format(b))

      result_type = self.cubo_seman.typematch(primitive_a, op, primitive_b)

      if (result_type == "error"):
        raise Exception('TYPE MISMATCH. {}({}) and {}({}) should be compatible through {} operation'.format(str(a),primitive_a,str(b),primitive_b,str(op)))

      return VarType(result_type)

  #estatutos
  def consume_arithmetic_op(self, op, a, b):
      result_type = self.validate_operation_and_get_result_type(op, a, b)

      result_temp_var = TuplaTablaVariables(
        name=self.quad_list.get_next_temp(),
        type=result_type,
        addr=self.get_addr(result_type, scope=self.current_scope))

      self.current_local_var_table[result_temp_var.name] = result_temp_var

      a_addr = self.resolve_address(a)
      b_addr = self.resolve_address(b)

      self.quad_list.add_quadd(get_instr_for_op(op), a_addr, b_addr, result_temp_var.addr)
      return result_temp_var.name

  def consume_relational_op(self, op, a, b):
    result_temp_var = TuplaTablaVariables(
      name=self.quad_list.get_next_temp(),
      type=VarType.BOOL,
      addr=self.get_addr(VarType.BOOL, scope=self.current_scope))

    self.current_local_var_table[result_temp_var.name] = result_temp_var
    a_addr = self.resolve_address(a)
    b_addr = self.resolve_address(b)

    self.validate_operation_and_get_result_type(op, a, b)

    self.quad_list.add_quadd(get_instr_for_op(op), a_addr, b_addr, result_temp_var.addr)
    return result_temp_var.name

  def consume_assignment(self, target, value):
    primitive_target = self.resolve_primitive_type(target)
    primitive_value = self.resolve_primitive_type(value)

    if (primitive_target != primitive_value):
      raise Exception('TYPE MISMATCH. {} can\'t be assigned to {}'.format(primitive_value, primitive_target))

    a_addr = self.resolve_address(value)
    b_addr = self.resolve_address(target)

    self.quad_list.add_quadd(Instruction.ASSIGN, a_addr, -1, b_addr)
    return target

  def consume_read(self, target):
    addr = self.resolve_address(target)
    self.quad_list.add_quadd(Instruction.READ, -1, -1, addr)

  def consume_write(self, value):
    addr = self.resolve_address(value)
    self.quad_list.add_quadd(Instruction.WRITE, -1, -1, addr)

  def start_if(self):
    self.quad_list.add_quadd(Instruction.JUMPF, -1, -1, -1)
    self.jump_stack.append(self.quad_list.pointer - 1)

  def end_if(self, cond):
    quad_to_update = self.jump_stack.pop()

    a_addr = self.resolve_address(cond)

    self.quad_list.update_target(quad_to_update, a_addr, None, self.quad_list.pointer)

  def start_else(self):
    self.quad_list.add_quadd(Instruction.JUMP, -1, -1, -1)
    self.jump_stack.append(self.quad_list.pointer - 1)

  def end_else(self, cond):
    else_start = self.jump_stack.pop()
    if_start = self.jump_stack.pop()

    cond_addr = self.resolve_address(cond)
    self.quad_list.update_target(if_start, cond_addr, None, else_start + 1)
    self.quad_list.update_target(else_start, None, None, self.quad_list.pointer)

  def start_while(self):
    self.jump_stack.append(self.quad_list.pointer - 1)
    self.quad_list.add_quadd(Instruction.JUMPF, -1, -1, -1)
    self.jump_stack.append(self.quad_list.pointer - 1)

  def end_while(self, cond):
    quad_to_update = self.jump_stack.pop()
    jump_on_false_quad = self.jump_stack.pop()
    self.quad_list.add_quadd(Instruction.JUMP, -1, -1, jump_on_false_quad)
    self.quad_list.update_target(quad_to_update, cond, None, self.quad_list.pointer)

  def start_do_while(self):
      quad_to_update = self.jump_stack.pop()
      jump_on_false_quad = self.jump_stack.pop()
      self.quad_list.add_quadd(Instruction.JUMP, -1, -1, jump_on_false_quad)
      self.quad_list.update_target(quad_to_update, self.quad_list.pointer)

  def end_do_while(self):
      quad_to_update = self.jump_stack.pop()
      jump_on_false_quad = self.jump_stack.pop()
      self.quad_list.add_quadd(Instruction.JUMP, -1, -1, jump_on_false_quad)
      self.quad_list.update_target(quad_to_update, self.quad_list.pointer)

  def start_for(self, asignacion, condicion):
      result_temp_var = TuplaTablaVariables(
        name=self.quad_list.get_next_temp(),
        type=VarType.BOOL,
        addr=self.get_addr(VarType.BOOL, scope=self.current_scope))

      assignment_addr = self.resolve_address(asignacion)
      cond_address = self.resolve_address(condicion)
      self.jump_stack.append(self.quad_list.pointer - 1) # Assignment quad
      self.jump_stack.append(self.quad_list.pointer ) # Cond quad
      self.quad_list.add_quadd(Instruction.SMLR_EQ, assignment_addr, cond_address, result_temp_var.addr)
      self.jump_stack.append(self.quad_list.pointer) # Jump quad
      self.quad_list.add_quadd(Instruction.JUMPF, result_temp_var.addr, -1, -1)

  def end_for(self):
    jump_quad = self.jump_stack.pop()
    cond_quad = self.jump_stack.pop()
    assignment_quad = self.jump_stack.pop()
    assignment_target_addr = self.quad_list.quadruples[assignment_quad][3]

    one_const_addr = self.resolve_address(1)
    self.quad_list.add_quadd(Instruction.PLUS, assignment_target_addr, one_const_addr, assignment_target_addr)
    self.quad_list.add_quadd(Instruction.JUMP, -1, -1, cond_quad)
    self.quad_list.update_target(jump_quad, None, None, self.quad_list.pointer)

  # Variables y funciones
  def start_global_var_declaration(self):
    self.current_local_var_table = self.global_var_table

  def start_func_scope_var_declaration(self, return_t, scope):
    self.current_scope = scope
    self.param_table[scope] = TuplaDirectorioFunciones(
      name=scope,
      return_type=return_t,
      param_table=[],
      param_pointers=[],
      local_variable_count = 0,
      start_pointer=self.quad_list.pointer+1)
    self.current_local_var_table = dict()

    if(return_t != 'void'):
      var_func = "var_func_" + scope
      self.current_scope = 'global'
      addr = self.get_addr(VarType(return_t), scope=self.current_scope)
      self.current_scope = scope
      self.global_var_table[var_func] = TuplaTablaVariables(
        name=var_func,
        type=VarType(return_t),
        addr=addr)

  def add_variable_to_current_scope(self, tipo, vars):
    var_type = VarType(tipo)

    for var in vars:
      (var_name, dim1, dim2) = var
      addr = None

      if dim1 != None and dim2 != None:
        addr = self.allocate_block(type=var_type, scope=self.current_scope, size=dim1*dim2)
      else:
        addr = self.get_addr(type=var_type, scope=self.current_scope)

      self.current_local_var_table[var_name] = TuplaTablaVariables(
        name=var_name,
        type=var_type,
        addr=addr,
        dims=(dim1, dim2))

  def add_param_to_current_scope(self, name, tipo):
    var_type = VarType(tipo)
    addr = self.get_addr(var_type, scope=self.current_scope)
    self.param_table[self.current_scope].param_table.append(var_type.value)
    self.param_table[self.current_scope].param_pointers.append(addr)
    self.current_local_var_table[name] = TuplaTablaVariables(name=name, type=var_type, addr=addr)

  def end_function_declaration(self):
    self.quad_list.add_quadd(Instruction.ENDFUN, -1, -1, -1)
    self.virtual_memory_manager.clear_mem()

  def verify_function_name(self, func_name):
    self.quad_list.reset_params()
    exists = self.param_table.get(func_name).name != None
    if not exists:
      raise Exception('Function {} does not exist'.format(func_name))
    self.quad_list.add_quadd(Instruction.ERA, -1, -1, func_name)


  def function_called(self, func_name, args):
    func_param_types = self.param_table.get(func_name).param_table
    func_param_pointers = self.param_table.get(func_name).param_pointers
    arg_count = len(args)
    expected_param_count = len(func_param_types)

    if arg_count != expected_param_count:
      raise Exception('Function {} was supplied {} arguments when {} parameters were declared.'.format(func_name, arg_count, expected_param_count))

    for i in range(0, arg_count):
      resolved_arg_type = self.resolve_primitive_type(args[i])
      value_addr = self.resolve_address(args[i])
      self.quad_list.add_quadd(Instruction.PARAM, -1, value_addr, func_param_pointers[i])
      if resolved_arg_type != func_param_types[i]:
        raise Exception('Expected {}, {} was supplied instead.'.format(func_param_types[i], resolved_arg_type))

    self.quad_list.add_quadd(Instruction.GOSUB, -1, -1, func_name)

    if 'var_func_' + func_name in self.global_var_table:
      return_var = self.resolve_var('var_func_' + func_name)
      result_temp_var = TuplaTablaVariables(
        name=self.quad_list.get_next_temp(),
        type=return_var.type,
        addr=self.get_addr(return_var.type, scope=self.current_scope))
      self.current_local_var_table[result_temp_var.name] = result_temp_var

      a_addr = return_var.addr
      b_addr = self.resolve_address(result_temp_var.name)
      self.quad_list.add_quadd(Instruction.ASSIGN, a_addr, -1, b_addr)
      return result_temp_var.name

  def first_quad(self):
    self.quad_list.add_quadd(Instruction.JUMP, -1, -1, 'MAIN')
    self.jump_stack.append(self.quad_list.pointer - 1)

  def principal(self):
    quad_to_update = self.jump_stack.pop()
    self.quad_list.update_target(quad_to_update, None, None, self.quad_list.pointer)

  def bind_return(self, value):
    a_addr = self.resolve_address(value)
    b_addr = self.resolve_address("var_func_" + self.current_scope)

    self.quad_list.add_quadd(Instruction.ASSIGN, a_addr, -1, b_addr)
    self.quad_list.add_quadd(Instruction.RETURN, -1, -1, b_addr)
    return b_addr

  def func_return(self, scope, value):
    expected_type = self.param_table[scope].return_type
    if value == None:
      return_value = None
    else:
      return_value = self.resolve_primitive_type(value)

    if expected_type != 'void':
      if return_value == None:
        raise Exception('{} function should return a value.'.format(expected_type))
      elif expected_type != return_value:
        raise Exception('TYPE MISMATCH. {} can\'t be assigned to {} function'.format(return_value,expected_type))
    elif return_value != None:
      raise Exception('Void function can not return a value.')
