import os,sys
from contextlib import contextmanager

#make temp mod directory

@contextmanager
def local_directory(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

script_dir = os.path.dirname(os.path.abspath(__file__))

with local_directory(script_dir):
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    #scripts
    from Scripts.Time import Time
    from Scripts.Commands import Commands