import PySimpleGUI as sg


def transform2D(transform_open):
    transform_open = not transform_open

    sg.theme("dark grey 9")

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Rotação", rotacaoLayout()),
                        sg.Tab("Translação", translacaoLayout()),
                        sg.Tab("Escalonamento", escalonamentoLayout()),
                    ]
                ]
            )
        ]
    ]

    window = sg.Window("Transformações", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            transform_open = not transform_open
            break

    window.close()


def rotacaoLayout():
    return [
        [
            sg.Column(
                [
                    [sg.Checkbox("Em torno do centro do mundo", k="-chkcentromundo-")],
                    [
                        sg.Checkbox(
                            "Em torno do centro do objeto", k="-chkcentroobjeto-"
                        )
                    ],
                    [sg.Checkbox("Em torno de um ponto qualquer", k="-chkpontoqlq-")],
                ]
            ),
            sg.Column(
                [
                    [
                        sg.Input("", enable_events=True, change_submits=True),
                        sg.Text("%"),
                    ],
                ]
            ),
        ]
    ]


def translacaoLayout():

    return [[]]


def escalonamentoLayout():

    return [[]]
