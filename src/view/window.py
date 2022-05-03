import PySimpleGUI as sg


def open_window():
    sg.theme("dark grey 9")

    active_button = "-select-"

    viewport_size = (600, 600)
    viewport_x = viewport_size[0] / 2
    viewport_y = viewport_size[1] / 2

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
                k="-viewport-",
            ),
            sg.Column(
                [
                    [
                        sg.Listbox(
                            values=items,
                            select_mode=sg.SELECT_MODE_EXTENDED,
                            size=(20, 40),
                        )
                    ]
                ],
                vertical_alignment="t",
            ),
        ],
    ]

    # Create the window
    window = sg.Window(
        "Graphics Computing", layout, use_default_focus=False, finalize=True
    )
    viewport = window["-viewport-"]

    # drawing vp line
    viewport.draw_line((0, -viewport_y), (0, viewport_y), color="red")  # origin
    viewport.draw_line((-viewport_x, 0), (viewport_x, 0), color="red")

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

        if event == "-viewport-":
            print("click on graph")

    window.close()


def menu_column():
    sz = (10, 1)
    return [
        [sg.Button("Select", size=sz, enable_events=True, k="-select-")],
        [sg.Button("Point", size=sz, enable_events=True, k="-point-")],
        [sg.Button("Line", size=sz, enable_events=True, k="-line-")],
        [sg.Button("Wireframe", size=sz, enable_events=True, k="-wireframe-")],
    ]
