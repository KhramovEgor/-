from Optimizer import optimize_ast
from ast_create import create_ast
from translator import load_ast_from_file, LLVMTranslator
import subprocess
import time

Opt = int(input("C оптимизации - 1, С Без оптимизации - 2 : "))

create_ast("input.txt", "ast.json")

optimize_ast("ast.json", "optimized_ast.json")

if Opt == 1:
    ast_filename = "optimized_ast.json"
else:
    ast_filename = "ast.json"

ast = load_ast_from_file(ast_filename)
translator = LLVMTranslator()
translator.translate_program(ast)
llvm_code = translator.generate_code()
with open("o.ll", "w") as output_file:
    output_file.write(llvm_code)

compile_command = ["clang", "o.ll", "-o", "o.exe"]
subprocess.run(compile_command, check=True)
executable_path = "./o.exe"
execute_command = [executable_path]
start_time = time.time()
subprocess.run(execute_command, check=True)

execution_time = time.time() - start_time
print("Execution time:", execution_time, "seconds")
