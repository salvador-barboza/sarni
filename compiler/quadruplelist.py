from enum import Enum
from typing import List

"""
Esta clase guarda la lista de cuadruplos, ademas funge el rol de asignar los nombres de las
variables temporales (t1, t2, t3, etc), parametros (param1, param2, ... paramN) y los pointers
(p1, p2, p3, etc).
"""
class QuadrupleList:
  quadruples = []
  current_temp = 0
  current_param = 0
  current_pointer = 0
  pointer = 0

  """
  Retorna el siguiente nombre de variable temporal (t1, t2, t3)
  """
  def get_next_temp(self):
    self.current_temp += 1
    return 't'+str(self.current_temp)

  """
  Retorna el siguiente nombre de variable pointer (p1, p2, p3)
  """
  def get_next_pointer(self):
    self.current_pointer += 1
    return 'p'+str(self.current_pointer)

  """
  Al salir de una funcion, se deben reiniciar los nombre de los parametros. Para eso se
  puede utilizar este metodo.
  """
  def reset_params(self):
    self.current_param = 0


  """
  Este metodo se utiliza para insertar un nuevo cuadruplo en la lista de cuadruplos y asi,
  no manipular directamente la lista. Cada vez que se agrega un cuadruplo, se incrementa el "pointer",
  que simplemente guarda el indice del pointer actual.
  """
  def add_quadd(self, a, b, c, d):
    self.pointer += 1
    self.quadruples.append((a, b, c, d))

  """
  Este metodo se utiliza para actualizar un cuadruplo que ya yabia sido añadido a la lista.
  Se debe pasar la direccion o indice del cuaruplo, asi como los valores a actualizar.
  Esto, se utiliza para actualizar jumpf, jump, etc.
  """
  def update_target(self, dir, a, b, c):
    old_tuple = self.quadruples[dir]
    new_tuple = (old_tuple[0], a or old_tuple[1], b or old_tuple[2], c or old_tuple[3])
    self.quadruples[dir] = new_tuple
