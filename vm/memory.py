from compiler.dirfunciones import VarType

class MemoryBlock:
  def __init__(self, start, end):
    self.start = start
    self.size = end - start
    self.seg_size = self.size // 4

    self.int = [None]* self.seg_size
    self.float = [None] * self.seg_size
    self.char = [None] * self.seg_size
    self.bool = [None] * self.seg_size

  def write(self, direct, value):
    real_addr = direct - self.start

    if 0  <= real_addr < self.seg_size:
      self.int[real_addr] = value
    elif self.seg_size  <= real_addr < self.seg_size * 2:
      self.float[real_addr] = value
    elif self.seg_size * 2  <= real_addr < self.seg_size * 3:
      self.char[real_addr] = value
    elif self.seg_size * 3  <= real_addr < self.seg_size * 4:
      self.bool[real_addr] = value


  def read(self, direct):
    real_addr = direct - self.start

    if 0  <= real_addr < self.seg_size:
      return self.int[real_addr]
    elif self.seg_size <= real_addr < self.seg_size * 2:
      return self.float[real_addr]
    elif self.seg_size * 2  <= real_addr < self.seg_size * 3:
      return self.char[real_addr]
    elif self.seg_size * 3  <= real_addr < self.seg_size * 4:
      return self.bool[real_addr]
