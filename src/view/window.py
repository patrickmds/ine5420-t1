import PySimpleGUI as sg


def open_window():
    sg.theme("dark grey 9")

    layout = [
        [
            sg.Column(menu_column(), vertical_alignment="t"),
            sg.Canvas(background_color="white", size=(600, 600), k="viewport"),
            sg.Column(item_list(), vertical_alignment="t"),
        ],
    ]

    # Create the window
    window = sg.Window("Column and Frame", layout)
    viewport = window["viewport"]

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


def item_list():
    # testando lista de itens
    return [
        [
            sg.Listbox(
                values=["1", "2", "3"],
                select_mode=sg.SELECT_MODE_EXTENDED,
                size=(20, 40),
            )
        ]
    ]
