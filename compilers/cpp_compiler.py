import subprocess
import tempfile
import os

def run_cpp_code(code: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        cpp_file = os.path.join(tmpdir, 'main.cpp')
        exe_file = os.path.join(tmpdir, 'main.out')
        with open(cpp_file, 'w') as f:
            f.write(code)
        compile_proc = subprocess.run(['g++', cpp_file, '-o', exe_file], capture_output=True, text=True)
        if compile_proc.returncode != 0:
            return compile_proc.stderr
        run_proc = subprocess.run([exe_file], capture_output=True, text=True)
        return run_proc.stdout + run_proc.stderr
