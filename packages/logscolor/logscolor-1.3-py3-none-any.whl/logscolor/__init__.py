import subprocess

def ejecutar_logscl(*args):
    result = subprocess.run(["./logscl", *args], capture_output=True, text=True)
    return result.stdout
