from .ML import *
import importlib as _importlib


submodules = [
    'tree',
]
def __dir__():
    return submodules

def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'matplobblib.ml.{name}')
