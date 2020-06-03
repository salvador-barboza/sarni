from vm.memory import MemoryBlock
from dataclasses import dataclass
from shared.memory_size import GLOBAL_MEMORY_BOUNDS, LOCAL_MEMORY_BOUNDS, \
  CONST_MEMORY_BOUNDS, TEMP_MEMORY_BOUNDS, POINTER_MEMORY_BOUND
from shared.instruction_set import Instruction
import numpy

"""
Esta clase se utiliza para guardar el contexto de ejecucion.
Contiene la posicion del instruction pointer, ademas del bloque
de memoria local correspondiente.
"""
@dataclass
class Frame:
  IP: int
  memory: MemoryBlock

class VM:
  """
  Esta variable permite depurar el codigo, ejecutando una sola instruccion
  a la vez y esperando un endline del usuario para continuar a la siguiente instruccion.
  """
  debug_mode = False

  """
  Desde 26 hasta 39, se pueden ver los pasos que se utilizan para inicializar la maquina virtual.
  Primero, se definen 2 bloques de memoria, uno para la global y otro para la de apuntadores,
  utilizando las constantes de tamaño que se encuentran en shared.memory_size.
  Despues, se crea un stack de frames con unn unico frame con su instruction pointer vacio y una nueva memoria. Este contexto o frame representa al contexto "global" de ejecucion.
  La variable next_frame es un temporal que se utiliza para guardar el "nuevo" contexto,
  momentos antes de hacer el cambio de contexto al ejecutar una funcion.
  En el metodo __init__ se requiere suministrar la lista de cuadruplos, el diccionario
  de constantes y el directorio de funciones.
  """
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

  """
  Este metodo se utiliza para entrar en el modo de depuracion. Cuando se activa,
  se imprimen todos los cuadruplos y el directorio de funciones.
  """
  def __inspect__(self):
    print(self.constant_memory)
    print(self.func_dir)
    self.debug_mode = True

    i = 0
    for quad in self.quads:
      print(str(i) + str(quad))
      i+=1

  """
  Este metodo es el que comienza la ejecucion del programa. Es un ciclo cuya condicion
  de terminacion es que el IP sea mayor a la lista de cuadruplos.
  """
  def run(self):
    print("Inicio:")
    while self.get_current_frame().IP < len(self.quads):
      self.next_instruction()

  """
  Este metodo se utiliza para ejecutar la instrucion actual.
  Primero, se extraen los valores del cuadruplo, teniendo
  instruccion, A, B, C.
  La instruccion despues se pasa a traves de un switch donde se
  determina la accion a ejecutar.
  En operaciones aritmeticas simplemente se leen los dos operandos (VER METODO read())
  y se escribe en la direccion C (VER METODO write()).
  Para el resto de las instrucciones, se muestra el detalle para cada caso:
  """
  def next_instruction(self):
    frame = self.get_current_frame()
    (instruction, A, B, C) = self.quads[frame.IP]

    if (self.debug_mode):
      print(">>>", frame.IP, instruction, A, B, C, "<<<")
      input()

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
      """
      ADD_ADDR se utiliza para el manejo de arreglos. La razon para la que se utilize este
      en vez de PLUS es que en este caso, se debe hacer un suma literal de A mas el valor de B.
      La suma normal, resolveria antes valores antes de sumarlo. Ademas, esta suma
      guarda el resultado directamente en la memoria de pointers.
      """
      self.pointer_memory.write(C, A + self.read(B))
    elif instruction == Instruction.VER:
      """
      VER verifica si la expresion A se encuentra entre B y C. Primero, se resuelve el valor
      de A, despues se pasa a int para soportar acceso a arreglos con floats (el comportamiento
      default es truncar el numero). Se arroja un error en caso de que estas dimensiones
      no sean respetadas.
      """
      int_index = int(self.read(A))
      if not B <= int_index < C:
        raise Exception('index {} out of range {}-{}'.format(int_index, B, C))
    elif instruction == Instruction.WRITE:
      """
      WRITE se utiliza para imprimir en pantalla. Primero se resuelve el valor de C,
      despues, en caso de imprimir un letrero, se deben des-escapar los saltos de linea
      para que estos sean impresos correctamente. Despues, se hace un print nativo de python.
      """
      val_to_print = self.read(C)
      if (type(val_to_print) == str):
        val_to_print = val_to_print.replace('\\n', '\n')
      print(val_to_print, end = '')
    elif instruction == Instruction.READ:
      """
      READ se utiliza para leer de la terminal. Para esto, se debe hacer primero un cast
      del string de entrada a su correspondiente valor. Despues, se escribe el valor
      en la direccion C.
      """
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
      """
      JUMP mueve el instruction pointer al cuadruplo C.
      """
      frame.IP = C
      return
    elif instruction == Instruction.JUMPF:
      """
      JUMP mueve el instruction pointer al cuadruplo C en caso de que le valor almacenado en A
      sea falso.
      """
      if self.read(A) == False:
        frame.IP = C
        return
    elif instruction == Instruction.ERA:
      """
      ERA se utiliza para preparar el nuevo contexto de ejecucion para una llamada de funcion.
      Primero se busca el inicio de la funcion (buscando en el directorio de funciones la entrada)
      para la funcion de nombre C. Luego, se especifica el tamaño del frame.
      (VER start_new_frame). start_new_frame guarda este nuevo frame en la variable temporal
      next_frame, donde este frame espera en lo que se realiza el cambio de contexto.
      """
      self.curr_param_pointer = 0
      self.start_new_frame(
        IP=self.func_dir[C].start_pointer-1,
        frame_size=6000
      )
    elif instruction == Instruction.PARAM:
      """
      Esta funcion se utiliza para mapear los valores para el parametro C en el contexto
      de ejecucion proximo a despertar.
      """
      self.next_frame.memory.write(C, self.read(B))
    elif instruction == Instruction.GOSUB:
      """
      Despues de crear el frame y mapear los valores para los parametros,
      se compienza a ejecutar la funcion. Para esto se llama la funcion auxiliar
      switch_to_new_frame, que simplemente agrega el next_frame al stack de contextos/frames
      y vacia la variable temporal next_frame.
      """
      frame.IP+=1
      self.switch_to_new_frame()
      return
    elif instruction == Instruction.ENDFUN:
      """
      Al terminar la ejecucion de una funcion, se despierta la memoria anterior, haciendo
      un pop del stack de la lista de contextos, eliminando la memoria alocada por la llamada
      de la funcion que acaba de concluir.
      """
      self.restore_past_frame()
      return
    elif instruction == Instruction.RETURN:
      """
      Al igual que ENFUN, RETURN despierta al contexto anterior y elimina la memoria alocada por la
      llamada de la funcion que acaba de retornar.
      """
      self.restore_past_frame()
      return
    elif instruction == Instruction.MATR_ADD:
      """
      Los cuadruplos de las operaciones matriciales tienen un formato diferente al resto.
      Como se puede ver, cada elemento contiene la direccion y el tamaño de la variable involucrada.
      (Operando A, B y la matriz para guardar el resultado).
      Para la suma, solamente se recorren los espacios y se suma cada elemento de A y B
      y se guarda en C.
      """
      (a_addr, a_dim1, a_dim2) = A
      (b_addr, b_dim1, b_dim2) = B
      (c_addr, c_dim1, c_dim2) = C

      size = a_dim1 * a_dim2

      for i in range(0, size):
        self.write(c_addr + i, self.read(a_addr + i) + self.read(b_addr + i))
    elif instruction == Instruction.MAT_SUB:
      """
      De la misma forma que en la suma, los cuadruplos contienen la direccion y tamaño de cada matriz.
      Y de igual manera, se resta cada elemento de A con B y se guarda en C.
      """
      (a_addr, a_dim1, a_dim2) = A
      (b_addr, b_dim1, b_dim2) = B
      (c_addr, c_dim1, c_dim2) = C

      size = a_dim1 * a_dim2

      for i in range(0, size):
        self.write(c_addr + i, self.read(a_addr + i) - self.read(b_addr + i))

    elif instruction == Instruction.MAT_MULT:
      """
      La multiplicacion de matrices se trata de una manera distinta a la de la suma y la resta de matrices.
      En este caso, no recorremos elemento por elemento, si no que utilizamos el metodo read_block de los MemoryBlocks
      para leer el bloque entero de memoria. En el cuadruplo, se almacena la direccion, ademas de las dimensiones de las
      matrices. Con estos datos, se puede determinar el tamaño del bloque de memoria a leer y se utiliza el metodo
      reshape de numpy para tomar este bloque de 1xsize y transformarlo en una matriz de dimensiones a_dim1xa_dim2, en el caso de
      la matriz A. Lo mismo sucede con B.
      Ya que se tienen ambas matrices, hacemos la multiplicacion con .matmul y se aplana el resultado, para asi poderlo guardar en
      C, elemento por elemento.
      """
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
      """
      Para la asignacion de una matriz o arreglo, se utiliza una tecnica similar a la de la suma y la resta,
      donde se recorre A y se asigna el valor de cada casilla de A en cada casilla de C.
      """
      (a_addr, a_size) = A
      (c_addr, c_size) = C

      for i in range(0, a_size):
        self.write(c_addr + i, self.read(a_addr + i))
    elif instruction == Instruction.DETERMINANTE:
      """
      Similar a como se hace con la multiplicacion de matrices, los cuadruplos para DETERMINANTE contienen
      las dimenciones de la matriz A. Con esto, utilizando read_block se puede reconsturir la matriz
      y utilizar el metodo .det de numpy para calcular el determinante. Despues se guarda este valor en C.
      """
      (a_addr, a_dim1, a_dim2) = A
      a_size = a_dim1 * a_dim2
      mat_a = self.read_block(a_addr, a_size)
      mat_a = numpy.reshape(mat_a, (a_dim1, a_dim2), order='C')
      self.write(C, numpy.linalg.det(mat_a))
    elif instruction == Instruction.TRANSPOSE:
      """
      Similar a como se hace con la multiplicacion de matrices, los cuadruplos para TRANSPOSE contienen
      las dimenciones de la matriz A y para la matriz C. Con esto, utilizando read_block se puede reconsturir la matriz
      y utilizar el metodo .transpose() para calcular la matriz traspuesta. Despues, se aplana esta matriz en una forma
      1xsize y se guarda, elemento por elemento, en C.
      """
      (a_addr, a_dim1, a_dim2) = A
      (c_addr, c_dim1, c_dim2) = C
      size = a_dim1 * a_dim2

      mat_a = self.read_block(a_addr, size)
      mat_a = numpy.reshape(mat_a, (a_dim1, a_dim2), order='C')
      res = mat_a.transpose().reshape(size)

      for i in range(0, size):
        self.write(c_addr + i, res[i])
    elif instruction == Instruction.INVERSA:
      """
      Similar a como se hace con la multiplicacion de matrices, los cuadruplos para INVERSA contienen
      las dimenciones de la matriz A. Con esto, utilizando read_block se puede reconsturir la matriz
      y utilizar el metodo .inv() para calcular la matriz traspuesta. Despues, se aplana esta matriz en una forma
      1xsize y se guarda, elemento por elemento, en C.
      """
      (a_addr, a_dim1, a_dim2) = A
      (c_addr, c_dim1, c_dim2) = C
      size = a_dim1 * a_dim2

      mat_a = self.read_block(a_addr, size)
      mat_a = numpy.reshape(mat_a, (a_dim1, a_dim2), order='C')
      res = numpy.linalg.inv(mat_a).reshape(size)

      for i in range(0, size):
        self.write(c_addr + i, res[i])

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


  """
  Esta funcion auxiliar se utiliza para abstaer la complejidad de las distintas memorias de la maquina virtual.
  Para escribir, solo se necesita especificar la direccion y el valor deseado. Con esto, esta funcion determina
  a que MemoryBlock debe escribir. Esta funcion tiene 2 casos especiales:
  1) Si se trata de escribir a memoria constante, entonces se arrojara un error, ya que esta memoria no es para
  escritura. Esto se valida en tiempo de compilacion, pero en caso de haber un error, aqui se detectaria tambien.
  2) En caso de escribir a una direccion de apuntador, primero se tiene que resolver la direccion a la que
  apunta este apuntador y despues, se escribe a esa direccion.
  """
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

  """
  Al igual que write, esta abstraccion permite no especificar a que MemoryBlock se desea escribir.
  Solo se necesita determinar la direccion y esta determinara de que memoria sacar los datos.
  Para los pointers, aqui primero se tiene que resolver la direccion a la que apunta el pointer.
  Despues, se retorna el valor que alamacena esa direccion.
  """
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

  """
  Al igual que read, esta abstraccion permite no especificar a que MemoryBlock se desea escribir.
  Solo se necesita determinar la direccion y el tamaño del bloque que se necesita.
  El leer un bloque de constantes no esta permitido, entonces este arroja un error.
  Para los pointers, aqui primero se tiene que resolver la direccion a la que apunta el pointer.
  Despues, se retorna el bloque al que este pointer apunta.
  """
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

