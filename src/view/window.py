import PySimpleGUI as sg


def open_window():
    sg.theme("dark grey 9")

    viewport_size = (600, 600)
    top_right = (300, 300)
    bottom_left = (-300, -300)

    items = []

    layout = [
        [
            sg.Column(menu_column(), vertical_alignment="t"),
            sg.Graph(
                canvas_size=viewport_size,
                graph_bottom_left=bottom_left,
                graph_top_right=top_right,
                background_color="white",
                border_width=1,
                k="viewport",
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
    window = sg.Window("Graphics Computing", layout, finalize=True)
    viewport = window["viewport"]

    # drawing vp line
    viewport.draw_line((0, -300), (0, 300))  # origin
    viewport.draw_line((-300, 0), (300, 0))

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        elif event == "select":
            print("select op is selected")
        elif event == "point":
            print("point op is selected")
        elif event == "line":
            print("line op is selected")
        elif event == "wireframe":
            print("wireframe op is selected")

    window.close()


def menu_column():
    # coluna com botões das funcionalidades
    sz = (10, 1)
    return [
        [sg.Button("Select", size=sz, k="select")],
        [sg.Button("Point", size=sz, k="point")],
        [sg.Button("Line", size=sz, k="line")],
        [sg.Button("Wireframe", size=sz, k="wireframe")],
    ]
