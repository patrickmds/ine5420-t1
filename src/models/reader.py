import os
import sys
from enums.obj_type import Obj_type
from models.object import DObject


class Reader:
    def read_file(self, file):
        lines = None
        with open(file) as f:
            lines = f.readlines()
        return self.read_objects(lines)

    def read_vertexes(self, open_file):
        vertex_list = []
        for index, line in enumerate(open_file):
            if line[0] != "v":
                continue
            _, x, y, z = line.strip('\n').split(' ')
            vertex_list.append((float(x), float(y), float(z)))
        return vertex_list

    def read_objects(self, open_file):
        objects = []
        reading = False
        vertexes = self.read_vertexes(open_file)
        current_obj = None

        for line in open_file:
            if line[0] != "o" and not reading:
                continue
            if line[0] == "o":
                reading = True
                _, name = line.strip("\n").split(" ")
                current_obj = DObject(name)
            else:
                if not line[0] in [v.value for n, v in Obj_type.__members__.items()]:
                    continue
                obj_type, *edges = line.strip("\n").split(" ")
                current_obj.obj_type = Obj_type(obj_type)
                current_obj.vertexes = [vertexes[int(i)-1] for i in edges]
                reading = False
                objects.append(current_obj)
        return objects
