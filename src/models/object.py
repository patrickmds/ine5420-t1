from enums.obj_type import Obj_type
class DObject:
    
    def __init__(self, name, obj_type=None, vertexes=None):
        self.name = name
        self.obj_type = obj_type
        self.vertexes = vertexes

    def draw(self, viewport):
        if self.obj_type == Obj_type.POINT:
            self.draw_point(viewport)
        if self.obj_type == Obj_type.LINE:
            self.draw_line(viewport)
        if self.obj_type == Obj_type.WIREFRAME:
            self.draw_wireframe(viewport)
    
    def draw_point(self, viewport):
        x, y, _ = self.vertexes[0]
        point = viewport.draw_point((x, y), color="red")

        return {
            "name": self.name,
            "id": point,
            "type": "point",
            "x": x,
            "y": y,
        }

    def draw_line(self, viewport):
        line = viewport.draw_line(self.vertexes[0], self.vertexes[1], color="red", width=2)
        return {
            "name": self.name,
            "id": line,
            "type": "line",
            "x": self.vertexes[0],
            "y": self.vertexes[1],
        }

    def draw_wireframe(self, viewport):
        pass