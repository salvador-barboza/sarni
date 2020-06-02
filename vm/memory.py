from compiler.dirfunciones import VarType

class MemoryBlock:
  def __init__(self, start, end):
    self.start = start
    self.size = end - start
    self.seg_size = self.size // 4

    self.int = [None] * self.seg_size
    self.float = [None] * self.seg_size
    self.char = [None] * self.seg_size
    self.bool = [None] * self.seg_size

  def write(self, direct, value):
    real_addr = direct - self.start

    if self.is_in_int_range(real_addr):
      self.int[self.get_int_addr(real_addr)] = value
    elif self.is_in_float_range(real_addr):
      self.float[self.get_float_addr(real_addr)] = value
    elif self.is_in_char_range(real_addr):
      self.char[self.get_char_addr(real_addr)] = value
    elif self.is_in_bool_range(real_addr):
      self.bool[self.get_bool_addr(real_addr)] = value

  def read(self, direct):
    real_addr = direct - self.start

    if self.is_in_int_range(real_addr):
      return self.int[self.get_int_addr(real_addr)]
    elif self.is_in_float_range(real_addr):
      return self.float[self.get_float_addr(real_addr)]
    elif self.is_in_char_range(real_addr):
      return self.char[self.get_char_addr(real_addr)]
    elif self.is_in_bool_range(real_addr):
      return self.bool[self.get_bool_addr(real_addr)]

  def read_block(self, direct, size):
    real_addr = direct - self.start
    if self.is_in_int_range(real_addr):
      return self.int[self.get_int_addr(real_addr) : self.get_int_addr(real_addr) + size]
    elif self.is_in_float_range(real_addr):
      return self.float[self.get_float_addr(real_addr) : self.get_float_addr(real_addr) + size]
    elif self.is_in_char_range(real_addr):
      return self.char[self.get_char_addr(real_addr) : self.get_char_addr(real_addr) + size]
    elif self.is_in_bool_range(real_addr):
      return self.bool[self.get_bool_addr(real_addr) : self.get_bool_addr(real_addr) + size]


  def is_in_int_range(self, addr): return 0 <= addr < self.seg_size
  def is_in_float_range(self, addr): return self.seg_size <= addr < self.seg_size * 2
  def is_in_char_range(self, addr): return self.seg_size * 2  <= addr < self.seg_size * 3
  def is_in_bool_range(self, addr): return self.seg_size * 3  <= addr < self.seg_size * 4

  def get_int_addr(self, addr): return addr
  def get_float_addr(self, addr): return addr - self.seg_size
  def get_char_addr(self, addr): return addr - self.seg_size * 2
  def get_bool_addr(self, addr): return addr - self.seg_size * 3
