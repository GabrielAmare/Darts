import sys
import os

PYTHON_EXECUTABLE_PATH = sys.executable

PIP = f"{PYTHON_EXECUTABLE_PATH} -m pip install {{}}"

commands = [
    PIP.format("--upgrade pip"),
    PIP.format("-i https://test.pypi.org/simple/ TextEngine"),
    PIP.format("-i https://test.pypi.org/simple/ tklib37"),
    PIP.format("-i https://test.pypi.org/simple/ PyAudio")
]

def main():
    for command in commands:
        os.system(command)


if __name__ == '__main__':
    main()
