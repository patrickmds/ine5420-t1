import PySimpleGUI as sg


def open_window():
    sg.theme("dark grey 9")

    active_button = "-select-"

    viewport_step = 50
    viewport_size = (600, 600)
    viewport_x = viewport_size[0] // 2
    viewport_y = viewport_size[1] // 2

    top_right = (viewport_x, viewport_y)
    bottom_left = (-viewport_x, -viewport_y)

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
                k="-viewport-",
            ),
            sg.Column(
                [
                    [
                        sg.Listbox(
                            values=items,
                            select_mode=sg.SELECT_MODE_EXTENDED,
                            size=(30, 40),
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

    viewport = window["-viewport-"]
    viewport.bind("<Button-1>", "+LEFT+")

    # drawing vp line
    draw_graph_axis_and_ticks(viewport, viewport_x, viewport_y, viewport_step)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break
        elif event in [
            "-select-",
            "-point-",
            "-line-",
            "-wireframe-",
        ]:
            window.find_element(active_button).update(button_color="white")
            active_button = event
            window.find_element(active_button).update(button_color="yellow")

        if event.startswith("-viewport-"):
            x, y = values["-viewport-"]

            if active_button == "-point-" and event.endswith("+LEFT+"):
                viewport.draw_point((x, y), 5, color="red")
                items.append({"type": "point", "x": x, "y": y})
                window.find_element("-itemlist-").update(values=items)

    window.close()


def menu_column():
    sz = (10, 1)
    return [
        [sg.Button("Select", size=sz, enable_events=True, k="-select-")],
        [sg.Button("Point", size=sz, enable_events=True, k="-point-")],
        [sg.Button("Line", size=sz, enable_events=True, k="-line-")],
        [sg.Button("Wireframe", size=sz, enable_events=True, k="-wireframe-")],
    ]


def draw_graph_axis_and_ticks(viewport, viewport_x, viewport_y, step):
    min_x = -viewport_x
    max_x = viewport_x

    min_y = -viewport_y
    max_y = viewport_y

    viewport.draw_line((0, min_y), (0, max_y), color="black")
    viewport.draw_line((min_x, 0), (max_x, 0), color="black")

    for x in range(min_x, max_x + 1, step):
        viewport.draw_line((x, -3), (x, 3))

    for y in range(min_y, max_y + 1, step):
        viewport.draw_line((-3, y), (3, y))
