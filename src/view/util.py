import PySimpleGUI as sg


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
        for line in lines:
            start, end = line["start"], line["end"]
            viewport.delete_figure(line["id"])
            n_line = viewport.draw_line(start, end, color="red", width=2)
            line["id"] = n_line


def update_item_list(window: sg.Window, items):
    values = [it["name"] for it in items]
    window.find_element("-itemlist-").update(values=values)


def draw_graph_axis_and_ticks(viewport: sg.Graph, top_right, bottom_left, step):
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
