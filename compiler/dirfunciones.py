from dataclasses import dataclass
from enum import Enum

"""
Este enum se utiliza para definir los tipos de variable que pueden existir en nuestro
compilador.
"""
class VarType(Enum):
  INT = 'int'
  CHAR = 'char'
  FLOAT = 'float'
  BOOL = 'bool'

"""
Este enum se utiliza para definir los tipos de retorno que una funcion puede tener.
"""
class ReturnType(Enum):
  VOID = 'void'
  INT = 'int'
  CHAR = 'char'
  FLOAT = 'float'

"""
Se utiliza para almacenar los datos de una variable en la tabla de variables.
name: nombre de la variable
type: un VarType que especifica el tipo
addr: la direccion de la variable, en el caso de matrices y arreglos es la direccion en donde
este empieza.
dims: las dimensiones de la variable. En el caso de una variable normal, estos son None, None.
En arreglos, la segunda dimension debe ser none y en matrices, ambas dimensiones deben tener un
valor definido.
"""
@dataclass
class TuplaTablaVariables:
    name: str
    type: VarType
    addr: int
    dims: (int, int) = (None, None)

"""
Se utilzia para almacenar los datos de una funcion en el directorio de funciones.
name: el nombre de la funcion
return_type: es el tipo de retorno de la funcion.
param_table: esta lista guarda los parametros para poder validar las llamadas a la funcion.
param_pointers: esta lista guarda las direcciones de los parametros de la funcion.
local_variable_count: guarda el numero de variables locales que fueron definidas en la funcion.
start_pointer: guarda en cual cuadruplo empieza esta funcion.
"""
@dataclass
class TuplaDirectorioFunciones:
    name: str
    return_type: ReturnType
    param_table: list
    param_pointers: list
    local_variable_count: int
    start_pointer: int
