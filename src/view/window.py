import PySimpleGUI as sg
from view.util import scale_when_zoom


def open_window():
    sg.theme("dark grey 9")

    active_button = "-select-"

    viewport_step = 50
    viewport_size = viewport_default_size = (600, 600)
    viewport_x = viewport_size[0] // 2
    viewport_y = viewport_size[1] // 2

    top_right = default_top_right = (viewport_x, viewport_y)
    bottom_left = default_bottom_left = (-viewport_x, -viewport_y)

    items = []

    layout = [
        [
            sg.Column(menu_column(), vertical_alignment="t", k="-buttons-"),
            sg.Graph(
                canvas_size=viewport_size,
                graph_bottom_left=bottom_left,
                graph_top_right=top_right,
                background_color="white",
                border_width=1,
                enable_events=True,
                drag_submits=True,
                motion_events=True,
                k="-viewport-",
            ),
            sg.Column(
                [
                    [
                        sg.Listbox(
                            values=items,
                            select_mode=sg.SELECT_MODE_EXTENDED,
                            size=(40, 40),
                            enable_events=True,
                            right_click_menu=["&Right", ["Delete"]],
                            k="-itemlist-",
                        )
                    ]
                ],
                vertical_alignment="t",
            ),
            sg.Column(
                [
                    [
                        sg.Button(
                            "zoom in",
                            size=(20, 10),
                            button_color="white",
                            enable_events=True,
                            k="-zoom-in-",
                        )
                    ],
                    [
                        sg.Button(
                            "zoom out",
                            size=(20, 10),
                            button_color="white",
                            enable_events=True,
                            k="-zoom-out-",
                        )
                    ],
                    [
                        sg.Button(
                            "Reset",
                            size=(20, 10),
                            button_color="white",
                            enable_events=True,
                            k="-reset-",
                        ),
                    ],
                ],
                vertical_alignment="t",
            ),
        ],
    ]

    # Create the window
    window = sg.Window("CG", layout, use_default_focus=False, finalize=True)

    window.find_element(active_button).update(button_color="yellow")

    viewport: sg.Graph = window["-viewport-"]
    viewport.bind("<Button-1>", "+LEFT")
    viewport.bind("<Button-4>", "-WHEEL")
    viewport.bind("<Button-5>", "+WHEEL")
    # viewport.bind("<MouseWheel>", "-WHEEL")

    # drawing vp line
    id_comp_axis = draw_graph_axis_and_ticks(
        viewport, viewport_x, viewport_y, viewport_step
    )

    drawing = False
    vertex_number = 0
    line_ids = []
    start_point = end_point = None
    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window
        # print(event)
        if event == sg.WIN_CLOSED:
            break

        if (
            event == "-zoom-in-"
            and all(
                x > y for x, y in zip(viewport_size, (viewport_step, viewport_step))
            )
            is True
        ):
            """Event to zoom in the viewport"""
            viewport_size = (
                viewport_size[0] - viewport_step,
                viewport_size[1] - viewport_step,
            )

            viewport_x = viewport_size[0] // 2
            viewport_y = viewport_size[1] // 2

            top_right = (viewport_x, viewport_y)
            bottom_left = (-viewport_x, -viewport_y)

            for line in id_comp_axis:
                viewport.delete_figure(line)
            viewport.change_coordinates(bottom_left, top_right)
            id_comp_axis = draw_graph_axis_and_ticks(
                viewport, viewport_x, viewport_y, viewport_step
            )
            for figure in items:
                scale_when_zoom(viewport, True, figure, viewport_step)

        if (
            event == "-zoom-out-"
            and all(x < y for x, y in zip(viewport_size, viewport_default_size)) is True
        ):
            """Event to zoom out the viewport"""
            viewport_size = (
                viewport_size[0] + viewport_step,
                viewport_size[1] + viewport_step,
            )

            viewport_x = viewport_size[0] // 2
            viewport_y = viewport_size[1] // 2

            top_right = (viewport_x, viewport_y)
            bottom_left = (-viewport_x, -viewport_y)

            for line in id_comp_axis:
                viewport.delete_figure(line)
            viewport.change_coordinates(bottom_left, top_right)
            id_comp_axis = draw_graph_axis_and_ticks(
                viewport, viewport_x, viewport_y, viewport_step
            )
            for figure in items:
                scale_when_zoom(viewport, False, figure, viewport_step)

        if event == "-reset-":
            """Event to reset the viewport"""
            items = []
            window.find_element("-itemlist-").update(values=items)
            viewport.erase()
            viewport.change_coordinates(default_bottom_left, default_top_right)
            draw_graph_axis_and_ticks(viewport, viewport_x, viewport_y, viewport_step)

        if event in [
            "-select-",
            "-point-",
            "-line-",
            "-wireframe-",
        ] and not drawing:
            window.find_element(active_button).update(button_color="white")
            active_button = event

            if start_point is not None and drawing is True:
                """Clean unfinished lines"""
                it = viewport.get_figures_at_location(start_point)
                print(it)
                for id in it:
                    viewport.delete_figure(id)
                drawing = False
                start_point = end_point = lastxy = None

            window.find_element(active_button).update(button_color="yellow")

        if event == "Delete":
            """Event to delete elements from sidelist"""
            for item in values["-itemlist-"]:
                if item['type'] == 'wireframe':
                    for line in item['id']:
                        viewport.delete_figure(line)
                    items.remove(item)
                    break
                viewport.delete_figure(item["id"])
                items.remove(item)
            window.find_element("-itemlist-").update(values=items)

        if event.startswith("-viewport-"):
            """Event ocurring inside viewport"""
            x, y = values["-viewport-"]
            # print(x, y, event)

            if active_button == "-point-" and event.endswith("+LEFT"):
                """Event to plot a point from mouse click"""
                point = viewport.draw_point((x, y), size=2, color="red")
                items.append({"id": point, "type": "point", "x": x, "y": y})
                window.find_element("-itemlist-").update(values=items)

            if active_button == "-line-":
                """Event to plot a line"""
                if event.endswith("+LEFT") and not drawing:
                    """Start drawing a line"""
                    start_point = (x, y)
                    drawing = True
                    line = viewport.draw_line(
                        start_point, start_point, color="blue", width=2
                    )
                    lastxy = x, y

                elif event.endswith("+UP") and (start_point != lastxy) and drawing:
                    """End drawing a line"""
                    end_point = (x, y)
                    viewport.delete_figure(line)
                    line = viewport.draw_line(
                        start_point, end_point, color="red", width=2
                    )
                    drawing = False
                    items.append(
                        {
                            "id": line,
                            "type": "line",
                            "start": start_point,
                            "end": end_point,
                        }
                    )
                    window.find_element("-itemlist-").update(values=items)

                elif drawing:
                    """Event while drawing a line"""
                    lastxy = x, y
                    viewport.delete_figure(line)
                    line = viewport.draw_line(
                        start_point, lastxy, color="blue", width=2
                    )
            if active_button == "-wireframe-":
                if not event.endswith("+MOVE"):
                    print(event)
                if event.endswith("+LEFT") and not drawing:
                    if vertex_number == 0:
                        first_point = x, y
                    start_point = x, y
                    drawing = True
                    line = viewport.draw_line(
                        start_point, start_point, color="blue", width=2
                    )
                    lastxy = x, y
                    vertex_number +=1
                elif event.endswith("+UP") and is_close_enough(first_point, (x, y)) and drawing and vertex_number > 2:
                    end_point = (x, y)
                    viewport.delete_figure(line)
                    wire_line = viewport.draw_line(start_point, first_point, color="red", width=2)
                    line_ids.append(wire_line)
                    drawing = False
                    items.append({"id": line_ids, "type": "wireframe", "start": start_point, "end": first_point})
                    window.find_element("-itemlist-").update(values=items)
                    vertex_number = 0
                elif event.endswith("+UP") and (start_point != lastxy) and not is_close_enough(first_point, (x, y)) and drawing:
                    end_point = x, y
                    viewport.delete_figure(line)
                    wire_line = viewport.draw_line(start_point, end_point, color="red", width=2)
                    line_ids.append(wire_line)
                    start_point = end_point
                    vertex_number +=1
                elif drawing:
                    lastxy = x, y
                    viewport.delete_figure(line)
                    line = viewport.draw_line(
                        start_point, lastxy, color="blue", width=2
                    )

    window.close()


def is_close_enough(first_point, second_point):
    return abs(first_point[0]-second_point[0]) < 5 and abs(first_point[1]-second_point[1]) < 5

def menu_column():
    sz = (10, 1)
    return [
        [
            sg.Button(
                "Select",
                size=sz,
                button_color="white",
                enable_events=True,
                k="-select-",
            )
        ],
        [
            sg.Button(
                "Point", size=sz, button_color="white", enable_events=True, k="-point-"
            )
        ],
        [
            sg.Button(
                "Line", size=sz, button_color="white", enable_events=True, k="-line-"
            )
        ],
        [
            sg.Button(
                "Wireframe",
                size=sz,
                button_color="white",
                enable_events=True,
                k="-wireframe-",
            )
        ],
    ]


def draw_graph_axis_and_ticks(viewport: sg.Graph, viewport_x, viewport_y, step):
    min_x = -viewport_x
    max_x = viewport_x

    min_y = -viewport_y
    max_y = viewport_y

    id_comp_axis = []

    xaxis = viewport.draw_line((min_x, 0), (max_x, 0), color="black")
    yaxis = viewport.draw_line((0, min_y), (0, max_y), color="black")

    id_comp_axis.append(xaxis)
    id_comp_axis.append(yaxis)

    for x in range(min_x, max_x + 1, step):
        xline = viewport.draw_line((x, -3), (x, 3))
        id_comp_axis.append(xline)
        if x != 0 and x != max_x:
            text = viewport.draw_text(x, (x, -10), color="black", font="helvetica 8")
            id_comp_axis.append(text)

    for y in range(min_y, max_y + 1, step):
        yline = viewport.draw_line((-3, y), (3, y))
        id_comp_axis.append(yline)
        if y != 0 and y != max_y:
            text = viewport.draw_text(y, (-15, y), color="black", font="helvetica 8")
            id_comp_axis.append(text)

    return id_comp_axis
