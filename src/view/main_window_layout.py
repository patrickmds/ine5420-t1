import PySimpleGUI as sg


def createMainLayout(
    items,
    pos,
    viewport_size,
    bottom_left,
    top_right,
    button_size,
    direction_button_size,
):
    return [
        [sg.Menu([["&File", ["&Open", "---", "&Exit"]]])],
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
                            element_justification="center",
                            expand_y=True,
                        )
                    ],
                    [
                        sg.Column(
                            [
                                [
                                    sg.Button(
                                        "up",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-up-",
                                    )
                                ],
                                [
                                    sg.Button(
                                        "left",
                                        size=direction_button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-left-",
                                    ),
                                    sg.Button(
                                        "right",
                                        size=direction_button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-right-",
                                    ),
                                ],
                                [
                                    sg.Button(
                                        "down",
                                        size=button_size,
                                        button_color="white",
                                        enable_events=True,
                                        k="-down-",
                                    ),
                                ],
                            ],
                            vertical_alignment="top",
                            element_justification="center",
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
                element_justification="center",
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
                            right_click_menu=["&Right", ["Delete"]],
                            k="-itemlist-",
                        )
                    ]
                ],
                vertical_alignment="t",
            ),
        ],
    ]
