from enums.obj_type import Obj_type
class DObject:
    
    def __init__(self, name, obj_type=None, vertexes=None):
        self.name = name
        self.obj_type = obj_type
        self.vertexes = vertexes

    def draw(self, viewport):
        if self.obj_type == Obj_type.POINT:
            return self.draw_point(viewport)
        if self.obj_type == Obj_type.LINE:
            return self.draw_line(viewport)
        if self.obj_type == Obj_type.WIREFRAME:
            return self.draw_wireframe(viewport)
    
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
        lines = []
        for v in range(len(self.vertexes)):
            if v == 0:
                continue
            line = viewport.draw_line(self.vertexes[v-1], self.vertexes[v], color="red", width=2)
            lines.append({
                "name": self.name + ('' if v==1 else str(v-1)),
                "id": line,
                "type": "line",
                "x": self.vertexes[v-1],
                "y": self.vertexes[v],
            })
        return lines

    def draw_wireframe(self, viewport):
        pass