from compiler.output_marshaling import CompilerOutput, write_compiler_output
from compiler.lexer import CalcLexer
from compiler.parser import CalcParser
import sys

lexer = CalcLexer()
parser = CalcParser()

with open(sys.argv[1], 'r') as file:
  program = file.read()
  parser.parse(lexer.tokenize(program))

  output = CompilerOutput(
    quadruples = parser.action_handler.quad_list.quadruples,
    constants = parser.action_handler.constant_map,
    func_dir = parser.action_handler.param_table
  )

  write_compiler_output(output, sys.argv[2])