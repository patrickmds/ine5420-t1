import PySimpleGUI as sg


def redraw_when_zoom(viewport: sg.Graph, figure):
    type = figure["type"]
    if type == "point":
        viewport.delete_figure(figure["id"])
        n_id = viewport.draw_point((figure["x"], figure["y"]), color="red")
        figure["id"] = n_id

    elif type == "line":
        start_line, end_line = figure["start"], figure["end"]
        viewport.delete_figure(figure["id"])
        n_line = viewport.draw_line(start_line, end_line, color="red", width=2)
        figure["id"] = n_line

    elif type == "wireframe":
        lines = figure["lines"]
        for line in lines:
            start_wireline, end_wireline = line["start"], line["end"]
            viewport.delete_figure(line["id"])
            n_wireline = viewport.draw_line(
                start_wireline, end_wireline, color="red", width=2
            )
            line["id"] = n_wireline


def update_item_list(window: sg.Window, items):
    values = [it["name"] for it in items]
    window.find_element("-itemlist-").update(values=values)


def draw_graph_axis_and_ticks(viewport: sg.Graph, viewport_x, viewport_y, step):
    min_x = -viewport_x
    max_x = viewport_x

    min_y = -viewport_y
    max_y = viewport_y

    id_comp_axis = []

    xaxis = viewport.draw_line((min_x, 0), (max_x, 0), color="lightgray")
    yaxis = viewport.draw_line((0, min_y), (0, max_y), color="lightgray")

    id_comp_axis.append(xaxis)
    id_comp_axis.append(yaxis)

    for x in range(min_x, max_x + 1, step):
        xline = viewport.draw_line((x, -3), (x, 3), color="lightgray")
        id_comp_axis.append(xline)

    for y in range(min_y, max_y + 1, step):
        yline = viewport.draw_line((-3, y), (3, y), color="lightgray")
        id_comp_axis.append(yline)

    return id_comp_axis


def is_close_enough(first_point, second_point):
    return (
        abs(first_point[0] - second_point[0]) < 5
        and abs(first_point[1] - second_point[1]) < 5
    )
