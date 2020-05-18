from compiler.output_marshaling import read_compiler_output
import sys

compiler_output = read_compiler_output(sys.argv[1])
print(compiler_output.constants)
print(compiler_output.func_dir)

i = 0
for quad in compiler_output.quadruples:
  i+=1
  print(str(i) + str(quad))