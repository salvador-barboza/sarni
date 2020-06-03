from compiler.dirfunciones import VarType


"""
Esta clase modela un bloque de memoria. Estos, son utilizados para definir
todos los tipos de memoria: la global, la local, la temporal y la de apuntadores.
En nuestro diseño, usamos 4 arreglos para representar los 4 tipos de memoria que hay.
Como constructor podemos ver que se pasa
start: el inicio de las direcciones para esta memoria
end: el fin de las direcciones para esta memoria
A partir de esos 2 parametros, se determina la longitud de espacios de memoria, a partir del
delta de estos.
Para determinar el tamaño real de cada particion de memoria, se utiliza como default el tamaño
de la memoria sobre 4, para tener 4 particiones iguales. Sin embargo, se puede
especificar el numero de elementos que cada particion debe tener. Esto, es utilizado cuando
se crea la memoria local para una funcion y se especifica el tamaño del ERA.
"""
class MemoryBlock:
  def __init__(self, start, end, real_seg_size = None):
    self.start = start
    self.size = end - start
    self.seg_size = self.size // 4

    if (real_seg_size == None):
      real_seg_size = self.seg_size

    self.int = [None] * real_seg_size
    self.float = [None] * real_seg_size
    self.char = [None] * real_seg_size
    self.bool = [None] * real_seg_size


  """
  Esta funcion, se utiliza para escribir en una direccion dentro del bloque de memoria.
  Para hacer esto, primero se determina la direccion real a la cual se debe escribir,
  siendo esto la direccion solicitada - la direccion de inicio de esta memoria.
  Despues, se determina a que particion se debe escribir (int, float, etc.) y se asigna el valor.
  Como soportamos operaciones entre floats e ints, se debe hacer la conversion a int y float
  respectivamente, para asi guardar valores validos siempre.
  """
  def write(self, direct, value):
    real_addr = direct - self.start

    if self.is_in_int_range(real_addr):
      self.int[self.get_int_addr(real_addr)] = int(value)
    elif self.is_in_float_range(real_addr):
      self.float[self.get_float_addr(real_addr)] = float(value)
    elif self.is_in_char_range(real_addr):
      self.char[self.get_char_addr(real_addr)] = value
    elif self.is_in_bool_range(real_addr):
      self.bool[self.get_bool_addr(real_addr)] = value

  """
  De manera muy similar a la de write(), para leer, se necesita primero determinar la direccion
  real utilizando el metodo descrito en la funcion write(). Una vez determinada esta direccion,
  se debe determinar la particion correcta a la cual se debe acceder. Despues, solaente
  se retorna el valor almacenado en la casilla especificada de la particion requerida.
  """
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

  """
  Para las operaciones con arreglos y matrices, se necesitan leer bloques de memoria completos.
  Este metodo de acceso toma la direccion del bloque y extra de la particion correspondiente un
  bloque del tamaño size. Este sub arreglo se puede utilizar despues para recrear
  la forma de la matriz requerida, ya que esta lista contendra las casillas de la matriz
  en manera plana, o es decir, como una lista.
  """
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


  """
  Las siguientes 8 funciones se utilizan para determinar si una direccion
  es int, float, char, o bool. Tambien se utilizan para resolver la direccion real de
  estos.
  """
  def is_in_int_range(self, addr): return 0 <= addr < self.seg_size
  def is_in_float_range(self, addr): return self.seg_size <= addr < self.seg_size * 2
  def is_in_char_range(self, addr): return self.seg_size * 2  <= addr < self.seg_size * 3
  def is_in_bool_range(self, addr): return self.seg_size * 3  <= addr < self.seg_size * 4

  def get_int_addr(self, addr): return addr
  def get_float_addr(self, addr): return addr - self.seg_size
  def get_char_addr(self, addr): return addr - self.seg_size * 2
  def get_bool_addr(self, addr): return addr - self.seg_size * 3
