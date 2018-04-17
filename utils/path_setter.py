import os

def set_path(file_name):
    return os.path.join(*[os.path.dirname(__file__), '..', 'templates', file_name])
