import numpy
from enums.obj_type import Obj_type


class DObject:
    def __init__(self, name, obj_type=None, vertexes=None):
        self.name = name
        self.obj_type = obj_type
        self.vertexes = vertexes

    def draw(self, viewport, viewport_size=None, top_right=None, bottom_left=None):
        if self.obj_type == Obj_type.POINT:
            return self.draw_point(viewport)
        if self.obj_type == Obj_type.LINE:
            return self.draw_line(viewport)
        if self.obj_type == Obj_type.WIREFRAME:
            return self.draw_wireframe(viewport)
        if self.obj_type == Obj_type.WORLD:
            return self.draw_world(viewport, viewport_size, top_right, bottom_left)
    
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
            line = viewport.draw_line(
                self.vertexes[v - 1], self.vertexes[v], color="red", width=2
            )
            lines.append(
                {
                    "name": self.name + ("" if v == 1 else str(v - 1)),
                    "id": line,
                    "type": "line",
                    "start": self.vertexes[v - 1],
                    "end": self.vertexes[v],
                }
            )
        return lines

    def draw_wireframe(self, viewport):
        line_ids = []
        wireframe_tuples = []

        for curr, nxt in zip(self.vertexes[0:], self.vertexes[1:]):
            curr_x, curr_y, _ = curr
            next_x, next_y, _ = nxt

            start_point = (curr_x, curr_y)
            end_point = (next_x, next_y)

            wire_line = viewport.draw_line(start_point, end_point, color="red", width=2)
            line_ids.append(wire_line)
            wireframe_tuples.append(
                {"id": wire_line, "start": start_point, "end": end_point}
            )

        sx, sy, _ = self.vertexes[0]
        lx, ly, _ = self.vertexes[-1]
        start_point = (lx, ly)
        end_point = (sx, sy)

        wire_line = viewport.draw_line(start_point, end_point, color="red", width=2)
        line_ids.append(wire_line)
        wireframe_tuples.append(
            {"id": wire_line, "start": start_point, "end": end_point}
        )

        return {
            "name": self.name,
            "id": line_ids,
            "type": "wireframe",
            "lines": wireframe_tuples,
        }

    def draw_world(self, viewport, viewport_size, top_right, bottom_left):
        viewport.change_coordinates(self.vertexes[0], self.vertexes[1])
        bl_x, bl_y, _ = self.vertexes[0]
        tr_x, tr_y, _ = self.vertexes[1]
        bottom_left = (bl_x, bl_y)
        top_right = (tr_x, tr_y)
        viewport_size = (tr_x - bl_x, tr_y - bl_y)
        return viewport_size, top_right, bottom_left