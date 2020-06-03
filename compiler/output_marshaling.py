from dataclasses import dataclass
from compiler.dirfunciones import TuplaDirectorioFunciones
import pickle

"""
Esta dataclass se utiliza para almacenar de una manera serializada
la lista de cuadruplos, el directorio de funcinoes y el mapa de constantes para
poder inicializar la maquina virtual.
"""
@dataclass
class CompilerOutput:
  quadruples: []
  constants: dict()
  func_dir: [TuplaDirectorioFunciones]


"""
A este metodo se le pasa la salida del compilador (un CompilerOutput) y se guarda en un archivo binario utilizando Pickle como herramienta de serializacion.
"""
def write_compiler_output(output, destination):
  outfile = open(destination, 'wb')
  pickle.dump(output, outfile)
  outfile.close()

"""
Esta herramienta toma un archivo binario serializado y lo deserializa utilizando pickle. Despues,
retorna el valor del CompilerOutpu que se encontraba en el archivo.
"""
def read_compiler_output(source):
  inputfile = open(source, 'rb')
  data: CompilerOutput = pickle.load(inputfile)
  inputfile.close()
  return data

