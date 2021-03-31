import os

print(os.getcwd())
print(os.path.dirname(os.path.realpath(__file__)))
print(os.pathsep + os.path.dirname(__file__))
