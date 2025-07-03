import subprocess
import tempfile
import os

def run_pascal_code(code: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        pas_file = os.path.join(tmpdir, 'main.pas')
        exe_file = os.path.join(tmpdir, 'main')
        with open(pas_file, 'w') as f:
            f.write(code)
        compile_proc = subprocess.run(['fpc', pas_file, '-o' + exe_file], capture_output=True, text=True)
        if compile_proc.returncode != 0:
            return compile_proc.stderr
        run_proc = subprocess.run([exe_file], capture_output=True, text=True)
        return run_proc.stdout + run_proc.stderr
