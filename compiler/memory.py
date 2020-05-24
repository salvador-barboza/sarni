from compiler.dirfunciones import VarType
from shared.memory_size import GLOBAL_MEMORY_BOUNDS, LOCAL_MEMORY_BOUNDS, \
  TEMP_MEMORY_BOUNDS, CONST_MEMORY_BOUNDS, POINTER_MEMORY_BOUND

class MemoryBlock:
  def __init__(self, start, end):
    chunk_size = (end - start + 1) // 4

    self.int = start
    self.float = self.int + chunk_size
    self.char = self.float + chunk_size
    self.bool = self.char + chunk_size

  def next_int(self):
    next_val = self.int
    self.int += 1
    return next_val

  def next_float(self):
    next_val = self.float
    self.float += 1
    return next_val

  def next_char(self):
    next_val = self.char
    self.char += 1
    return next_val

  def next_bool(self):
    next_val = self.bool
    self.bool += 1
    return next_val

  def next_int_block(self, size):
    next_val = self.int
    self.int += size
    return next_val

  def next_float_block(self, size):
    next_val = self.float
    self.float += size
    return next_val

  def next_char_block(self, size):
    next_val = self.char
    self.char += size
    return next_val

  def next_bool_block(self, size):
    next_val = self.bool
    self.bool += size
    return next_val


  def next(self, type):
    if type == VarType.INT:
      return self.next_int()
    elif type == VarType.FLOAT:
      return self.next_float()
    elif type == VarType.CHAR:
      return self.next_char()
    elif type == VarType.BOOL:
      return self.next_bool()

  def allocate_block(self, type, size):
    print(size)
    if type == VarType.INT:
      return self.next_int_block(size)
    elif type == VarType.FLOAT:
      return self.next_float_block(size)
    elif type == VarType.CHAR:
      return self.next_char_block(size)
    elif type == VarType.BOOL:
      return self.next_bool_block(size)

class VirtualMemoryManager:
  def __init__(self):
    self.global_addr = MemoryBlock(GLOBAL_MEMORY_BOUNDS[0], GLOBAL_MEMORY_BOUNDS[1])
    self.local_addr = MemoryBlock(LOCAL_MEMORY_BOUNDS[0], LOCAL_MEMORY_BOUNDS[1])
    self.temp_addr = MemoryBlock(TEMP_MEMORY_BOUNDS[0], TEMP_MEMORY_BOUNDS[1])
    self.const_addr = MemoryBlock(CONST_MEMORY_BOUNDS[0], CONST_MEMORY_BOUNDS[1])
    self.pointer_addr = MemoryBlock(POINTER_MEMORY_BOUND[0], POINTER_MEMORY_BOUND[1])

  def clear_mem(self):
    self.temp_addr = MemoryBlock(TEMP_MEMORY_BOUNDS[0], TEMP_MEMORY_BOUNDS[1])
    self.local_addr = MemoryBlock(LOCAL_MEMORY_BOUNDS[0], LOCAL_MEMORY_BOUNDS[1])
