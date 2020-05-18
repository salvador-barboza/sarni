from vm.memory import MemoryBlock

class VM:
  global_memory = MemoryBlock(start=0, size=6000)
  temp_memory = MemoryBlock(start=6000, size=6000)

  IP = 0

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
      i+=1
      print(str(i) + str(quad))


  def run(self):
    print("Inicio:")
    while self.IP < len(self.quads):
      self.next_instruction()

  def next_instruction(self):
    (instruction, A, B, C) = self.quads[self.IP]
    if instruction == '+':
      self.write(C, self.read(A) + self.read(B))
      self.IP += 1
    elif instruction == '-':
      self.write(C, self.read(A) - self.read(B))
      self.IP += 1
    elif instruction == '*':
      self.write(C, self.read(A) * self.read(B))
      self.IP += 1
    elif instruction == '/':
      self.write(C, self.read(A) / self.read(B))
      self.IP += 1
    elif instruction == '=':
      self.write(C, self.read(A))
      self.IP += 1
    elif instruction == '==':
      self.write(C, self.read(A) == self.read(B))
      self.IP += 1
    elif instruction == '<':
      self.write(C, self.read(A) < self.read(B))
      self.IP += 1
    elif instruction == '>':
      self.write(C, self.read(A) > self.read(B))
      self.IP += 1
    elif instruction == 'WRITE':
      print(self.read(C))
      self.IP += 1
    elif instruction == 'JUMP':
      self.IP = C
      return
    elif instruction == 'JUMPF':
      if self.read(C) == False:
        self.IP = C
        return


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
