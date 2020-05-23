from compiler.output_marshaling import read_compiler_output
from vm.vm import VM
import sys

compiler_output = read_compiler_output(sys.argv[1])

vm = VM(
  quads=compiler_output.quadruples,
  constants=compiler_output.constants,
  func_dir=compiler_output.func_dir)

vm.__inspect__()
vm.run()