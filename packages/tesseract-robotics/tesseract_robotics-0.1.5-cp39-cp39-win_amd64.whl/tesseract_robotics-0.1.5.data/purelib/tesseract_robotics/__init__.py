import sys
import os

if sys.platform == 'win32':
    os.add_dll_directory(os.path.dirname(os.path.realpath(__file__)))
    os.environ["PATH"] += os.pathsep + os.path.dirname(os.path.realpath(__file__))
