from dataclasses import dataclass
from compiler.dirfunciones import TuplaDirectorioFunciones
import pickle

@dataclass
class CompilerOutput:
  quadruples: []
  constants: dict()
  func_dir: [TuplaDirectorioFunciones]


def write_compiler_output(output, destination):
  outfile = open(destination, 'wb')
  pickle.dump(output, outfile)
  outfile.close()

def read_compiler_output(source):
  inputfile = open(source, 'rb')
  data: CompilerOutput = pickle.load(inputfile)
  inputfile.close()
  return data

