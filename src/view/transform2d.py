import PySimpleGUI as sg
from numpy import double


def transform2D(transform_open, figure):
    sg.theme("dark grey 9")
    transform_open = not transform_open

    curr_op = "-rot-"
    rotacao_option = "-rtcrmundo-"

    rotacao_angle = dx_tran = dy_tran = sx_esc = sy_esc = None

    opindex = 0
    ops = {
        "figure": figure,
        "rot_ops": [],
        "tran_ops": [],
        "esc_ops": [],
    }
    allops = []

    log = []

    layout = [
        [
            sg.Column(
                [
                    [
                        sg.TabGroup(
                            [
                                [
                                    sg.Tab("Rotação", rotacaoLayout(), k="-rot-"),
                                    sg.Tab(
                                        "Translação", translacaoLayout(), k="-tran-"
                                    ),
                                    sg.Tab(
                                        "Escalonamento",
                                        escalonamentoLayout(),
                                        k="-esc-",
                                    ),
                                ]
                            ],
                            expand_x=True,
                        )
                    ],
                    [sg.Button("Salvar transformação", k="-salvar-")],
                    [
                        sg.Listbox(
                            values=log,
                            select_mode=None,
                            size=(60, 10),
                            k="-loglist-",
                        )
                    ],
                ],
                vertical_alignment="t",
            ),
            sg.Column(
                [
                    [
                        sg.Listbox(
                            values=allops,
                            select_mode=sg.SELECT_MODE_SINGLE,
                            size=(40, 20),
                            enable_events=True,
                            right_click_menu=["&Right", ["Delete"]],
                            k="-itemlist-",
                        )
                    ]
                ],
                vertical_alignment="t",
            ),
        ],
        [
            [sg.Button("Aplicar", k="-aplicar-")],
        ],
    ]

    window = sg.Window("Transformações", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            transform_open = not transform_open
            break

        if event in ["-rot-", "-tran-", "-esc-"]:
            curr_op = event

        if event in ["-rtctrmundo-", "-rtctrobjeto-", "-rtpontoqlq-"]:
            rotacao_option = event

        if event == "-angleinput-":
            try:
                rotacao_angle = double(values["-angleinput-"])
                window.find_element("-angleinput-").update(values["-angleinput-"])
            except Exception:
                log.append(
                    'Bad entry for input: "%s". Expecting only numbers (double)'
                    % values["-angleinput-"]
                )
                window.find_element("-loglist-").update(log)

        if event in ["-deslocxinput-", "-deslocyinput-"]:
            try:
                val = int(values[event])
                if event == "-deslocxinput-":
                    dx_tran = val
                else:
                    dy_tran = val
                window.find_element(event).update(values[event])
            except Exception:
                log.append(
                    'Bad entry for input: "%s". Expecting only numbers (int)'
                    % values[event]
                )
                window.find_element("-loglist-").update(log)

        if event in ["-escxinput-", "-escyinput-"]:
            try:
                val = int(values[event])
                if event == "-escxinput-":
                    sx_esc = val
                else:
                    sy_esc = val
                window.find_element(event).update(values[event])
            except Exception:
                log.append(
                    'Bad entry for input: "%s". Expecting only numbers (int)'
                    % values[event]
                )
                window.find_element("-loglist-").update(log)

        if event == "-salvar-":
            if curr_op == "-rot-":
                ops["rot_ops"].append(
                    {"ĩd": opindex, "angle": rotacao_angle, "on": rotacao_option}
                )
                allops.append(
                    {
                        "id": opindex,
                        "type": "rotacao",
                        "angulo": rotacao_angle,
                        "modo": rotacao_option,
                    }
                )
                opindex += 1
                rotacao_angle = None
                window.find_element("-itemlist-").update(allops)

            if curr_op == "-tran-":
                ops["tran_ops"].append({"id": opindex, "dx": dx_tran, "dy": dy_tran})
                allops.append(
                    {
                        "id": opindex,
                        "type": "translação",
                        "dx": dx_tran,
                        "dy": dy_tran,
                    }
                )
                opindex += 1
                dx_tran = dy_tran = None
                window.find_element("-itemlist-").update(allops)

            if curr_op == "-esc-":
                ops["esc_ops"].append({"id": opindex, "sx": sx_esc, "sy": sy_esc})
                allops.append(
                    {
                        "id": opindex,
                        "type": "escalonamento",
                        "sx": sx_esc,
                        "sy": sy_esc,
                    }
                )
                opindex += 1
                sx_esc = sy_esc = None
                window.find_element("-itemlist-").update(allops)

    window.close()


def rotacaoLayout():
    return [
        [
            sg.Column(
                [
                    [
                        sg.Radio(
                            "Em torno do centro do mundo",
                            "-rotGroup-",
                            k="-rtctrmundo-",
                            enable_events=True,
                            default=True,
                        )
                    ],
                    [
                        sg.Radio(
                            "Em torno do centro do objeto",
                            "-rotGroup-",
                            k="-rtctrobjeto-",
                            enable_events=True,
                        )
                    ],
                    [
                        sg.Radio(
                            "Em torno de um ponto qualquer",
                            "-rotGroup-",
                            k="-rtpontoqlq-",
                            enable_events=True,
                        )
                    ],
                ]
            ),
            sg.Column(
                [
                    [
                        sg.Input(
                            "",
                            size=(10, 10),
                            enable_events=True,
                            change_submits=True,
                            k="-angleinput-",
                        ),
                        sg.Text("º"),
                    ],
                ],
                vertical_alignment="t",
            ),
        ]
    ]


def translacaoLayout():
    return [
        [
            sg.Column(
                [
                    [
                        sg.Text("Dx"),
                        sg.Input(
                            "",
                            size=(10, 10),
                            enable_events=True,
                            change_submits=True,
                            k="-deslocxinput-",
                        ),
                    ],
                    [
                        sg.Text("Dy"),
                        sg.Input(
                            "",
                            size=(10, 10),
                            enable_events=True,
                            change_submits=True,
                            k="-deslocyinput-",
                        ),
                    ],
                ],
                vertical_alignment="t",
            ),
        ]
    ]


def escalonamentoLayout():
    return [
        [
            sg.Column(
                [
                    [
                        sg.Text("Sx"),
                        sg.Input(
                            "",
                            size=(10, 10),
                            enable_events=True,
                            change_submits=True,
                            k="-escxinput-",
                        ),
                    ],
                    [
                        sg.Text("Sy"),
                        sg.Input(
                            "",
                            size=(10, 10),
                            enable_events=True,
                            change_submits=True,
                            k="-escyinput-",
                        ),
                    ],
                ],
                vertical_alignment="t",
            ),
        ]
    ]
