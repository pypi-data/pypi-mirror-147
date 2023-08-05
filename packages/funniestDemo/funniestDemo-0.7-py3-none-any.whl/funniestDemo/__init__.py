import sys
from importlib import resources
print('__init__')
print('__init__.__name__', __name__)
print('__init__.__package__', __package__)
print('sys.path', sys.path)

def joke():
    with resources.open_text('funniestDemo', 'buddha.txt') as f:
        print(f.read())