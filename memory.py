from dirfunciones import VarType

class MemoryBlock:
  def __init__(self, chunk_size, start):
    self.int = start
    self.float = self.int + chunk_size
    self.char = self.float + chunk_size
    self.bool = self.char + chunk_size
    self.end = self.bool + chunk_size

    print(self.int, self.float, self.char, self.bool)

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


  def next(self, type):
    if type == VarType.INT:
      return self.next_int()
    elif type == VarType.FLOAT:
      return self.next_float()
    elif type == VarType.CHAR:
      return self.next_char()
    elif type == VarType.BOOL:
      return self.next_bool()


class VirtualMemoryManager:
  chunk_size = 1500

  def __init__(self):
    self.global_addr = MemoryBlock(self.chunk_size, 0)
    self.temp_addr = MemoryBlock(self.chunk_size, self.global_addr.end)
    self.const_addr = MemoryBlock(self.chunk_size, self.temp_addr.end)

  def clear_temp(self):
    self.temp_addr = MemoryBlock(self.chunk_size, self.global_addr.end)
