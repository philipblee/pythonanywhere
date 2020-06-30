import os
""" changes directory name to src folder for reading and writing
"""

def get_dir():
    dir_name = os.path.dirname(os.getcwd()) + '/src'
    os.chdir(dir_name)
    return