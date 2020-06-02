from vm.memory import MemoryBlock
from dataclasses import dataclass
from shared.memory_size import GLOBAL_MEMORY_BOUNDS, LOCAL_MEMORY_BOUNDS, \
  CONST_MEMORY_BOUNDS, TEMP_MEMORY_BOUNDS, POINTER_MEMORY_BOUND
from shared.instruction_set import Instruction
import numpy

@dataclass
class Frame:
  IP: int
  memory: MemoryBlock

class VM:
  global_memory = MemoryBlock(start=GLOBAL_MEMORY_BOUNDS[0], end=GLOBAL_MEMORY_BOUNDS[1])
  pointer_memory = MemoryBlock(start=POINTER_MEMORY_BOUND[0], end=POINTER_MEMORY_BOUND[1])

  frames = [Frame(IP=0,
    memory=MemoryBlock(start=LOCAL_MEMORY_BOUNDS[0], end=LOCAL_MEMORY_BOUNDS[1]))]
  next_frame: Frame = None

  def __init__(self, quads, constants, func_dir):
    self.quads = quads
    self.constant_memory = dict(map(lambda c : (c[1], c[0]), constants.values()))
    self.func_dir = func_dir
    self.curr_param_pointer = 0

  def __inspect__(self):
    print(self.constant_memory)
    print(self.func_dir)

    i = 0
    for quad in self.quads:
      print(str(i) + str(quad))
      i+=1

  def run(self):
    print("Inicio:")
    while self.get_current_frame().IP < len(self.quads):
      self.next_instruction()

  def next_instruction(self):
    frame = self.get_current_frame()
    (instruction, A, B, C) = self.quads[frame.IP]

    if instruction == Instruction.PLUS:
      self.write(C, self.read(A) + self.read(B))
    elif instruction == Instruction.MINUS:
      self.write(C, self.read(A) - self.read(B))
    elif instruction == Instruction.MULTIP:
      self.write(C, self.read(A) * self.read(B))
    elif instruction == Instruction.DIVISION:
      self.write(C, self.read(A) / self.read(B))
    elif instruction == Instruction.MOD:
      self.write(C, self.read(A) % self.read(B))
    elif instruction == Instruction.ASSIGN:
      self.write(C, self.read(A))
    elif instruction == Instruction.EQ:
      self.write(C, self.read(A) == self.read(B))
    elif instruction == Instruction.SMLR:
      self.write(C, self.read(A) < self.read(B))
    elif instruction == Instruction.SMLR_EQ:
      self.write(C, self.read(A) <= self.read(B))
    elif instruction == Instruction.GTR:
      self.write(C, self.read(A) > self.read(B))
    elif instruction == Instruction.GTR_EQ:
      self.write(C, self.read(A) >= self.read(B))
    elif instruction == Instruction.OR:
      self.write(C, self.read(A) or self.read(B))
    elif instruction == Instruction.AND:
      self.write(C, self.read(A) and self.read(B))
    elif instruction == Instruction.ADD_ADDR:
      self.pointer_memory.write(C, A + self.read(B))
    elif instruction == Instruction.VER:
      if not B <= self.read(A) < C:
        raise Exception('index {} out of range {}-{}'.format(self.read(A), B, C))
    elif instruction == Instruction.WRITE:
      val_to_print = self.read(C)
      if (type(val_to_print) == str):
        val_to_print = val_to_print.replace('\\n', '\n')
      print(val_to_print, end = '')
    elif instruction == Instruction.READ:
      x = input()
      if B == 'int':
        x = int(x)
      elif B == 'float':
        x = float(x)
      elif B == 'char':
        x = str(x)
      elif B == 'bool':
        x = bool(x)
      self.write(C,x)
    elif instruction == Instruction.JUMP:
      frame.IP = C
      return
    elif instruction == Instruction.JUMPF:
      if self.read(A) == False:
        frame.IP = C
        return
    elif instruction == Instruction.ERA:
      self.curr_param_pointer = 0
      self.start_new_frame(
        IP=self.func_dir[C].start_pointer-1,
        frame_size=6000
      )
    elif instruction == Instruction.PARAM:
      self.next_frame.memory.write(C, self.read(B))
    elif instruction == Instruction.GOSUB:
      frame.IP+=1
      self.switch_to_new_frame()
      return
    elif instruction == Instruction.ENDFUN:
      self.restore_past_frame()
      return
    elif instruction == Instruction.RETURN:
      self.restore_past_frame()
      return
    elif instruction == Instruction.MATR_ADD:
      (a_addr, a_size, _) = A
      (b_addr, b_size, _) = B
      (c_addr, c_size, _) = C

      for i in range(0, a_size):
        self.write(c_addr + i, self.read(a_addr + i) + self.read(b_addr + i))
    elif instruction == Instruction.MAT_SUB:
      (a_addr, a_size, _) = A
      (b_addr, b_size, _) = B
      (c_addr, c_size, _) = C

      for i in range(0, a_size):
        self.write(c_addr + i, self.read(a_addr + i) - self.read(b_addr + i))

    elif instruction == Instruction.MAT_MULT:
      (a_addr, a_dim1, a_dim2) = A
      (b_addr, b_dim1, b_dim2) = B
      (c_addr, c_dim1, c_dim2) = C

      a_size = a_dim1 * a_dim2
      b_size = b_dim1 * b_dim2
      c_size = a_dim1* b_dim2

      mat_a = self.read_block(a_addr, a_size)
      mat_a = (numpy.reshape(mat_a, (a_dim1, a_dim2), order='C'))
      mat_b = self.read_block(b_addr, b_size)
      mat_b = (numpy.reshape(mat_b, (b_dim1, b_dim2), order='C'))
      res = numpy.matmul(mat_a, mat_b).reshape(c_size)

      for i in range(0, c_size):
        self.write(c_addr + i, res[i])
    elif instruction == Instruction.MULT_DIM_ASSIGN:
      (a_addr, a_size) = A
      (c_addr, c_size) = C

      for i in range(0, a_size):
        self.write(c_addr + i, self.read(a_addr + i))
    elif instruction == Instruction.DETERMINANTE:
      (a_addr, a_dim1, a_dim2) = A
      a_size = a_dim1 * a_dim2
      mat_a = self.read_block(a_addr, a_size)
      mat_a = numpy.reshape(mat_a, (a_dim1, a_dim2), order='C')
      self.write(C, numpy.linalg.det(mat_a))

    frame.IP+=1

  def get_current_frame(self):
    return self.frames[len(self.frames) - 1]

  def start_new_frame(self, IP, frame_size):
    self.next_frame = Frame(IP=IP, memory=MemoryBlock(LOCAL_MEMORY_BOUNDS[0], LOCAL_MEMORY_BOUNDS[0] + frame_size))

  def switch_to_new_frame(self):
    self.frames.append(self.next_frame)
    self.next_frame = None

  def restore_past_frame(self):
    self.frames.pop()

  def write(self, direct, value):
    if GLOBAL_MEMORY_BOUNDS[0] <= direct < GLOBAL_MEMORY_BOUNDS[1]:
      self.global_memory.write(direct, value)
    elif LOCAL_MEMORY_BOUNDS[0] <= direct < LOCAL_MEMORY_BOUNDS[1]:
      self.get_current_memory().write(direct, value)
    elif CONST_MEMORY_BOUNDS[0] <= direct < CONST_MEMORY_BOUNDS[1]:
      raise MemoryError("Cannot to write to read-only memory")
    elif POINTER_MEMORY_BOUND[0] <= direct < POINTER_MEMORY_BOUND[1]:
      real_addr = self.pointer_memory.read(direct)
      self.write(real_addr, value)

  def read(self, direct):
    if GLOBAL_MEMORY_BOUNDS[0] <= direct < GLOBAL_MEMORY_BOUNDS[1]:
      return self.global_memory.read(direct)
    elif LOCAL_MEMORY_BOUNDS[0] <= direct < LOCAL_MEMORY_BOUNDS[1]:
      return self.get_current_memory().read(direct)
    elif CONST_MEMORY_BOUNDS[0] <= direct < CONST_MEMORY_BOUNDS[1]:
      return self.constant_memory[direct]
    elif POINTER_MEMORY_BOUND[0] <= direct < POINTER_MEMORY_BOUND[1]:
      real_addr = self.pointer_memory.read(direct)
      return self.read(real_addr)

  def read_block(self, direct, size):
    if GLOBAL_MEMORY_BOUNDS[0] <= direct < GLOBAL_MEMORY_BOUNDS[1]:
      return self.global_memory.read_block(direct, size)
    elif LOCAL_MEMORY_BOUNDS[0] <= direct < LOCAL_MEMORY_BOUNDS[1]:
      return self.get_current_memory().read_block(direct, size)
    elif CONST_MEMORY_BOUNDS[0] <= direct < CONST_MEMORY_BOUNDS[1]:
      raise MemoryError("Not implemented")
    elif POINTER_MEMORY_BOUND[0] <= direct < POINTER_MEMORY_BOUND[1]:
      real_addr = self.pointer_memory.read_block(direct, size)
      return self.read(real_addr)

  def get_current_memory(self):
    current_frame = self.get_current_frame()
    return current_frame.memory

