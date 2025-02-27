import os

"""" This module is responsible for reading the input file and returning the data in a structured format. """

path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

def read_input_file(file_name):
    file_path = os.path.join(path, 'data', file_name)
    with open(file_path, 'r') as file:
        state = [list(line.strip()) for line in file]
    file.close()
    return state
    