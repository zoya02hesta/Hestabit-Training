import sys
import subprocess
import tempfile
import os

code = "import pandas; print(f'Pandas version: {pandas.__version__}')"
with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
    tmp.write(code)
    tmp_path = tmp.name

print(f"Running with: {sys.executable}")
res = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True)
print(f"STDOUT: {res.stdout}")
print(f"STDERR: {res.stderr}")

os.unlink(tmp_path)
