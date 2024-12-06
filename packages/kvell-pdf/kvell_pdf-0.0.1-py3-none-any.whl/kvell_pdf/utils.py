import importlib


def import_package(name, package=None):
    try:
        module = importlib.import_module(name, package=package)
        return module
    except ModuleNotFoundError:
        return None