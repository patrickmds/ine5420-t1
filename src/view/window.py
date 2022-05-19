import PySimpleGUI as sg
from view.transform2d import transform2D
from view.util import (
    redraw_when_zoom,
    update_item_list,
    draw_graph_axis_and_ticks,
    is_close_enough,
)


def open_window():
    sg.theme("dark grey 9")

    active_button = "-select-"

    viewport_step = 50
    viewport_size = viewport_default_size = (600, 600)
    viewport_x = viewport_default_x = viewport_size[0] // 2
    viewport_y = viewport_default_y = viewport_size[1] // 2

    top_right = default_top_right = (viewport_x, viewport_y)
    bottom_left = default_bottom_left = (-viewport_x, -viewport_y)

    items = []
    point_index_gen = line_index_gen = wireframe_index_gen = 0

    button_size = (10, 1)

    pos = "-"

    layout = [
        [
            sg.Column(
                [
                    [
                        sg.Column(
                            [
                                [
                                    sg.Button(
                                        "Select",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-select-",
                                    )
                                ],
                                [
                                    sg.Button(
                                        "Point",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-point-",
                                    )
                                ],
                                [
                                    sg.Button(
                                        "Line",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-line-",
                                    )
                                ],
                                [
                                    sg.Button(
                                        "Wireframe",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-wireframe-",
                                    )
                                ],
                            ],
                            vertical_alignment="top",
                            expand_y=True,
                        )
                    ],
                    [
                        sg.Column(
                            [
                                [
                                    sg.Button(
                                        "Zoom +",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-zoom-in-",
                                    )
                                ],
                                [
                                    sg.Button(
                                        "Zoom -",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-zoom-out-",
                                    )
                                ],
                                [
                                    sg.Button(
                                        "Reset",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-reset-",
                                    ),
                                ],
                            ],
                        )
                    ],
                ],
                expand_y=True,
                k="-buttons-",
            ),
            sg.Column(
                [
                    [
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
                        )
                    ],
                    [sg.Text(text=pos, k="-pos-")],
                ],
            ),
            sg.Column(
                [
                    [
                        sg.Listbox(
                            values=items,
                            select_mode=sg.SELECT_MODE_SINGLE,
                            size=(20, 40),
                            enable_events=True,
                            right_click_menu=["&Right", ["Transform", "Delete"]],
                            k="-itemlist-",
                        )
                    ]
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
    wireframe_tuples = []
    start_point = end_point = first_point = unfinished_line = None

    transform_open = False

    # Create an event loop
    while True:

        event, values = window.read()
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

        if (
            event.startswith("-viewport-") is False
            and active_button in ["-line-", "-wireframe-"]
            and unfinished_line is not None
        ):
            """Removing unfinished draws"""
            viewport.delete_figure(unfinished_line)
            for line in wireframe_tuples:
                viewport.delete_figure(line["id"])

            drawing = False
            wireframe_tuples = line_ids = []
            start_point = end_point = lastxy = unfinished_line = first_point = None

        if event == "Transform" and transform_open is False:
            transform2D(transform_open, values["-itemlist-"])

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
                redraw_when_zoom(viewport, figure)

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
                redraw_when_zoom(viewport, figure)

        if event == "-reset-":
            """Event to reset the viewport"""
            items = []
            update_item_list(window, items)
            viewport.erase()
            viewport.change_coordinates(default_bottom_left, default_top_right)
            viewport_size = viewport_default_size
            viewport_x = viewport_default_x
            viewport_y = viewport_default_y
            id_comp_axis = draw_graph_axis_and_ticks(
                viewport, viewport_x, viewport_y, viewport_step
            )

        if event in [
            "-select-",
            "-point-",
            "-line-",
            "-wireframe-",
        ]:
            window.find_element(active_button).update(button_color="white")
            active_button = event
            window.find_element(active_button).update(button_color="yellow")

        if event == "Delete":
            """Event to delete elements from sidelist"""
            for item in items:
                if item["name"] in values["-itemlist-"]:
                    if item["type"] == "wireframe":
                        for line in item["id"]:
                            viewport.delete_figure(line)
                    else:
                        viewport.delete_figure(item["id"])
                    items.remove(item)
            update_item_list(window, items)
            window.refresh()

        if event.startswith("-viewport-"):
            """Event ocurring inside viewport"""
            x, y = values["-viewport-"]

            pos = f"({x}, {y})"
            window.find_element("-pos-").update(pos)

            if active_button == "-point-" and event.endswith("+LEFT"):
                """Event to plot a point from mouse click"""
                point = viewport.draw_point((x, y), color="red")
                point_index_gen += 1
                items.append(
                    {
                        "name": f"point_{point_index_gen}",
                        "id": point,
                        "type": "point",
                        "x": x,
                        "y": y,
                    }
                )
                update_item_list(window, items)

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
                    unfinished_line = line

                elif event.endswith("+UP") and (start_point != lastxy) and drawing:
                    """End drawing a line"""
                    end_point = (x, y)
                    viewport.delete_figure(line)
                    line = viewport.draw_line(
                        start_point, end_point, color="red", width=2
                    )
                    line_index_gen += 1
                    items.append(
                        {
                            "name": f"line_{line_index_gen}",
                            "id": line,
                            "type": "line",
                            "start": start_point,
                            "end": end_point,
                        }
                    )
                    drawing = False
                    unfinished_line = line = None
                    update_item_list(window, items)

                elif drawing:
                    """Event while drawing a line"""
                    lastxy = x, y
                    viewport.delete_figure(line)
                    line = viewport.draw_line(
                        start_point, lastxy, color="blue", width=2
                    )
                    unfinished_line = line

            if active_button == "-wireframe-":
                if event.endswith("+LEFT") and not drawing:
                    start_point = x, y
                    if vertex_number == 0:
                        first_point = start_point
                    drawing = True
                    line = viewport.draw_line(
                        start_point, start_point, color="blue", width=2
                    )
                    unfinished_line = line
                    lastxy = x, y
                    vertex_number += 1
                elif (
                    event.endswith("+UP")
                    and is_close_enough(first_point, (x, y))
                    and drawing
                    and vertex_number > 2
                ):
                    end_point = (x, y)
                    viewport.delete_figure(line)
                    wire_line = viewport.draw_line(
                        start_point, first_point, color="red", width=2
                    )
                    line_ids.append(wire_line)
                    wireframe_tuples.append(
                        {"id": wire_line, "start": start_point, "end": first_point}
                    )
                    drawing = False
                    wireframe_index_gen += 1
                    items.append(
                        {
                            "name": f"wireframe_{wireframe_index_gen}",
                            "id": line_ids,
                            "type": "wireframe",
                            "lines": wireframe_tuples,
                        }
                    )
                    print(wireframe_tuples)
                    update_item_list(window, items)
                    unfinished_line = first_point = None
                    wireframe_tuples = line_ids = []
                    vertex_number = 0
                elif (
                    event.endswith("+UP")
                    and (start_point != lastxy)
                    and not is_close_enough(first_point, (x, y))
                    and drawing
                ):
                    end_point = x, y
                    viewport.delete_figure(line)
                    wire_line = viewport.draw_line(
                        start_point, end_point, color="red", width=2
                    )
                    line_ids.append(wire_line)
                    wireframe_tuples.append(
                        {"id": wire_line, "start": start_point, "end": end_point}
                    )
                    start_point = end_point
                    vertex_number += 1
                elif drawing:
                    lastxy = x, y
                    viewport.delete_figure(line)
                    line = viewport.draw_line(
                        start_point, lastxy, color="blue", width=2
                    )
                    unfinished_line = line

    window.close()
