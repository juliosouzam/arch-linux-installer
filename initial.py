from subprocess import run

try:
    run(['ls', '-la'], check=True)
except Exception as ex:
    print(ex)
