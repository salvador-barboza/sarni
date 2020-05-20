from vm.memory import MemoryBlock
from dataclasses import dataclass

@dataclass
class Frame:
  IP: int
  params: dict



class VM:
  global_memory = MemoryBlock(start=0, size=6000)
  temp_memory = MemoryBlock(start=6000, size=6000)
  frames = [Frame(IP=0, params=dict())]
  next_frame = None

  def __init__(self, quads, constants, func_dir):
    self.quads = quads
    self.constants = constants
    self.constant_memory = dict(zip(constants.values(), constants.keys()))
    self.func_dir = func_dir

  def __inspect__(self):
    print(self.constants)
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

    if instruction == '+':
      self.write(C, self.read(A) + self.read(B))
    elif instruction == '-':
      self.write(C, self.read(A) - self.read(B))
    elif instruction == '*':
      self.write(C, self.read(A) * self.read(B))
    elif instruction == '/':
      self.write(C, self.read(A) / self.read(B))
    elif instruction == '=':
      self.write(C, self.read(A))
    elif instruction == '==':
      self.write(C, self.read(A) == self.read(B))
    elif instruction == '<':
      self.write(C, self.read(A) < self.read(B))
    elif instruction == '>':
      self.write(C, self.read(A) > self.read(B))
    elif instruction == 'WRITE':
      print(self.read(C))
    elif instruction == 'JUMP':
      frame.IP = C
      return
    elif instruction == 'JUMPF':
      if self.read(C) == False:
        frame.IP = C
        return
    elif instruction == 'ERA':
      self.start_new_frame(self.func_dir[C].start_pointer-1)
    elif instruction == 'PARAM':
      self.next_frame.params[C] = self.read(B)
      self.write(C, self.read(B))
    elif instruction == 'GOSUB':
      frame.IP+=1
      self.switch_to_new_frame()
      return
    elif instruction == 'RETURN':
      self.restore_past_frame()
      return

    frame.IP+=1



  def get_current_frame(self):
    return self.frames[len(self.frames) - 1]

  def start_new_frame(self, IP):
    self.next_frame = Frame(IP=IP, params=dict())

  def switch_to_new_frame(self):
    self.frames.append(self.next_frame)
    self.next_frame = None

  def restore_past_frame(self):
    self.frames.pop()
    for (direct, value) in self.get_current_frame().params.items():
      self.write(direct, value)



  def write(self, direct, value):
    if 0  <= direct < 6000:
      self.global_memory.write(direct, value)
    elif 6000 <= direct < 12000:
      self.temp_memory.write(direct, value)
    elif 12000 <= direct < 18000:
      raise MemoryError("Trying to write to memory")

  def read(self, direct):
    if 0  <= direct < 6000:
      return self.global_memory.read(direct)
    elif 6000 <= direct < 12000:
      return self.temp_memory.read(direct)
    elif 12000 <= direct < 18000:
      return self.constant_memory[direct]
