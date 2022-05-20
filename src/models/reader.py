import os
import sys

class Reader:
    
    #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__) + '/..'

    def read_vertexes(self, file=None):
        if (file):
            return self.read_line_type(file, 'v')
        with open(f'{self.ROOT_DIR}/{file}', 'r') as f:
            return self.read_line_type(f, 'v')

    def read_line_type(self, f, l_type):
        vertex_list = []
        for index, line in enumerate(f):
            if (line[0] != l_type):
                continue
            _, x, y, z = line.strip('\n').split(' ')
            vertex_list.append((index, x, y, z))
        return vertex_list
        