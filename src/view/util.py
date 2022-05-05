import PySimpleGUI as sg


def redraw_when_zoom(viewport: sg.Graph, figure):
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
