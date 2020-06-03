from compiler.dirfunciones import VarType
from shared.memory_size import GLOBAL_MEMORY_BOUNDS, LOCAL_MEMORY_BOUNDS, \
  TEMP_MEMORY_BOUNDS, CONST_MEMORY_BOUNDS, POINTER_MEMORY_BOUND

"""
Este MemoryBlock se utiliza para mantener el registro de variables que han sido asignadas y sus
direcciones en tiempo de compilacion. Como puede observarse, este MemoryBlock difiere de aquel del
paquete de VM en que este, no aloca ningun valor, si no, solo devuelve numeros para la siguiente
direccion disponible para el tipo que se solicite.
Esta clase contiene 4 "particiones" y cada una guarda la siguinete direccion disponible.
"""
class MemoryBlock:
  def __init__(self, start, end):
    chunk_size = (end - start + 1) // 4

    self.int = start
    self.float = self.int + chunk_size
    self.char = self.float + chunk_size
    self.bool = self.char + chunk_size

  """
  Los siguientes 4 metodos, se utilizan para resolver el siguiente valor
  disponible para valores int, float, char y bool.
  """
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

  """
  Los siguientes 4 metodos, se utilizan cuando se necesitan reservar bloques completos
  de memoria.
  """
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

  """
  Este metodo es el medio principal para obtener direcciones desde fuera de la clase.
  Este determina la particion de memoria de la cual se requiere asignar una direccion,
  y llama al metodo apropiado, retornando el valor de este.
  """
  def next(self, type):
    if type == VarType.INT:
      return self.next_int()
    elif type == VarType.FLOAT:
      return self.next_float()
    elif type == VarType.CHAR:
      return self.next_char()
    elif type == VarType.BOOL:
      return self.next_bool()

  """
  Al igual que next, este metodo esta diseñado para ser usado fuera de la clase, cuando
  se debe alocar un bloque completo de memoria. Se debe suministrar el tipo y el numero de casillas
  que se desean alocar. Este, devolvera la direccion de memoria inicial del bloque que se alocó.
  """
  def allocate_block(self, type, size):
    if type == VarType.INT:
      return self.next_int_block(size)
    elif type == VarType.FLOAT:
      return self.next_float_block(size)
    elif type == VarType.CHAR:
      return self.next_char_block(size)
    elif type == VarType.BOOL:
      return self.next_bool_block(size)

"""
Esta clase se utiliza para guardar los 5 espacios de memoria disponibles,
y tiene el metodo clear_mem que se utiliza para "reiniciar" los temporales y
variables locales de la memoria. clear_mem se llama cuando se termina de interpretar
la declaracion de una funcion.
"""
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
