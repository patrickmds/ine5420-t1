import PySimpleGUI as sg


def fileReader():
    sg.theme("dark grey 9")

    layout = [
        [
            sg.Text("Choose a file: "),
            sg.Input(),
            sg.FileBrowse(key="-IN-", file_types=(("Object files", "*.obj"),)),
        ],
        [sg.Button("Open")],
    ]

    window = sg.Window("Open file", layout, size=(520, 100))

    filepath = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Open":
            filepath = values["-IN-"]
            window.close()
            break

    return filepath
