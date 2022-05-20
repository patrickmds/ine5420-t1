import PySimpleGUI as sg
import numpy as np
from enums.obj_type import Obj_type


def draw_list(objects, viewport, items):
    world_changes = None
    for obj in objects:
        if obj.obj_type == Obj_type.WORLD:
            world_changes = obj.draw(viewport)
            for item in items:
                redraw_figures(viewport, item)
            continue
        drawn = obj.draw(viewport)
        if isinstance(drawn, list):
            for d in drawn:
                items.append(d)
        else:
            items.append(drawn)
    return world_changes


def redraw_figures(viewport: sg.Graph, figure):
    type = figure["type"]
    if type == "point":
        viewport.delete_figure(figure["id"])
        n_id = viewport.draw_point((figure["x"], figure["y"]), color="red")
        figure["id"] = n_id

    elif type == "line":
        start, end = figure["start"], figure["end"]
        viewport.delete_figure(figure["id"])
        n_line = viewport.draw_line(start, end, color="red", width=2)
        figure["id"] = n_line

    elif type == "wireframe":
        lines = figure["lines"]
        new_ids = []
        for line in lines:
            start, end = line["start"], line["end"]
            viewport.delete_figure(line["id"])
            n_line = viewport.draw_line(start, end, color="red", width=2)
            line["id"] = n_line
            new_ids.append(n_line)
        figure["id"] = new_ids


def update_item_list(window: sg.Window, items):
    values = [it["name"] for it in items]
    window.find_element("-itemlist-").update(values)


def draw_graph_axis_and_ticks(viewport: sg.Graph, top_right, bottom_left):
    id_comp_axis = []

    xaxis = viewport.draw_line(
        (bottom_left[0], 0), (top_right[0], 0), color="lightgray"
    )
    yaxis = viewport.draw_line(
        (0, bottom_left[1]), (0, top_right[1]), color="lightgray"
    )

    id_comp_axis.append(xaxis)
    id_comp_axis.append(yaxis)

    return id_comp_axis


def is_close_enough(first_point, second_point):
    return (
        abs(first_point[0] - second_point[0]) < 5
        and abs(first_point[1] - second_point[1]) < 5
    )


def translate(Dx, Dy):
    translattion_matrix = np.array([[1, 0, 0], [0, 1, 0], [Dx, Dy, 1]])
    return translattion_matrix


def scale(Sx, Sy):
    scaling_matrix = np.array([[Sx, 0, 0], [0, Sy, 0], [0, 0, 1]])
    return scaling_matrix


def rotate(angle: float):
    angle_in_radians = np.radians(-angle)
    cos = np.cos(angle_in_radians)
    sin = np.sin(angle_in_radians)
    rotation_matrix = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
    return rotation_matrix
