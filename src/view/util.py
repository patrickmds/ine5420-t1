import PySimpleGUI as sg


def scale_when_zoom(viewport: sg.Graph, plus, figure, step):
    type = figure["type"]
    if type == "point":
        if plus is True:
            x, y = zoom_in_coordinates((figure["x"], figure["y"]), step)
        else:
            x, y = zoom_out_coordinates((figure["x"], figure["y"]), step)
        viewport.relocate_figure(figure["id"], x, y)
        figure["x"] = x
        figure["y"] = y

    elif type == "line":
        start, end = figure["start"], figure["end"]
        if plus is True:
            n_start = zoom_in_coordinates(start, step)
            n_end = zoom_in_coordinates(end, step)
        else:
            n_start = zoom_out_coordinates(start, step)
            n_end = zoom_out_coordinates(end, step)
        viewport.delete_figure(figure["id"])
        n_line = viewport.draw_line(n_start, n_end, color="red", width=2)
        figure["start"] = n_start
        figure["end"] = n_end
        figure["id"] = n_line


def zoom_in_coordinates(point, step):
    x, y = point

    ret = (0, 0)
    if x > 0:
        x = x + step
        if y > 0:
            ret = (x, y + step)
        elif y < 0:
            ret = (x, y - step)
        else:
            ret = (x, 0)
    elif x < 0:
        x = x - step
        if y > 0:
            ret = (x, y + step)
        elif y < 0:
            ret = (x, y - step)
        else:
            ret = (x, 0)
    else:
        if y > 0:
            ret = (0, y + step)
        elif y < 0:
            ret = (0, y - step)

    return ret


def zoom_out_coordinates(point, step):
    x, y = point

    ret = (0, 0)
    if x > 0:
        x = x - step
        if y > 0:
            ret = (x, y - step)
        elif y < 0:
            ret = (x, y + step)
        else:
            ret = (x, 0)
    elif x < 0:
        x = x + step
        if y > 0:
            ret = (x, y - step)
        elif y < 0:
            ret = (x, y + step)
        else:
            ret = (x, 0)
    else:
        if y > 0:
            ret = (0, y - step)
        elif y < 0:
            ret = (0, y + step)

    return ret
