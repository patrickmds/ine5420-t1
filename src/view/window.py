import PySimpleGUI as sg


def open_window():
    sg.theme("dark grey 9")

    layout = [
        [
            sg.Column(menu_column(), vertical_alignment="t"),
            sg.Column([[sg.Text("Column1", background_color="red", size=(100, 40))]]),
            sg.Column(item_list(), vertical_alignment="t"),
        ],
    ]

    # Create the window
    window = sg.Window("Column and Frame", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()


def menu_column():
    # coluna com botões das funcionalidades
    sz = (10, 1)
    return [
        [sg.Button("Select", size=sz)],
        [sg.Button("Point", size=sz)],
        [sg.Button("Line", size=sz)],
        [sg.Button("Wireframe", size=sz)],
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
