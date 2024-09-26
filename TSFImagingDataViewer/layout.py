# The following code has been modified from pyMALDIproc/pyMALDIviz and flex_maldi_dda_automation.
# For more information, see the following links:
# https://github.com/gtluu/pymaldiproc
# https://github.com/gtluu/flex_maldi_dda_automation


from dash import dcc, html
import dash_bootstrap_components as dbc
from TSFImagingDataViewer.util import blank_figure


def get_dashboard_layout():
    """
    Get the dashboard layout for TSFImagingDataViewer.

    :return: Dash dashboard layout
    :rtype: html.Div
    """
    dashboard_layout = html.Div(
        [
            dcc.Loading(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    'Load Bruker *.d TSF Data',
                                    id='load_tsf',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'justify-content': 'center',
                                           'width': '95%'},
                                    disabled=False
                                ),
                                width=3
                            ),
                            dbc.Col(
                                dbc.Button(
                                    'View Average Estimate Spectrum',
                                    id='average_estimate',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'justify-content': 'center',
                                           'width': '95%'},
                                    disabled=True
                                ),
                                width=3
                            ),
                            dbc.Col(
                                dbc.Button(
                                    'View Full Average Spectrum',
                                    id='average_full',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'justify-content': 'center',
                                           'width': '95%'},
                                    disabled=True
                                ),
                                width=3
                            ),
                            dbc.Col(
                                dbc.Button(
                                    'View Individual Spectrum',
                                    id='per_frame',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'justify-content': 'center',
                                           'width': '95%'},
                                    disabled=True
                                ),
                                width=3
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id='ion_image',
                                    figure=blank_figure(),
                                    style={'width': '95%'}
                                ),
                                width=12
                            )
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText('m/z'),
                                        dbc.Input(
                                            id='mz',
                                            placeholder=0,
                                            value=0,
                                            type='number',
                                            min=0,
                                            max=0,
                                            step=0.00001,
                                            disabled=True
                                        )
                                    ],
                                    id='mz_group',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'width': '95%'}
                                ),
                                width={'size': 2, 'offset': 2}
                            ),
                            dbc.Col(
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText('m/z Tolerance'),
                                        dbc.InputGroupText(u"\u00B1"),
                                        dbc.Input(
                                            id='mz_tolerance',
                                            placeholder=0,
                                            value=0,
                                            type='number',
                                            min=0,
                                            max=1000000,
                                            step=0.00001,
                                            disabled=True
                                        ),
                                        dbc.Select(
                                            id='mz_tolerance_unit',
                                            options=[{'label': 'Da', 'value': 'Da'},
                                                     {'label': 'ppm', 'value': 'ppm'}],
                                            value='Da',
                                            disabled=True
                                        )
                                    ],
                                    id='mz_tolerance_group',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'width': '95%'}
                                ),
                                width=4
                            ),
                            dbc.Col(
                                dbc.Button(
                                    'Update Ion Image',
                                    id='update_ion_image',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'justify-content': 'center',
                                           'width': '95%'},
                                    disabled=True
                                ),
                                width=2
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText('X'),
                                        dbc.Input(
                                            id='x_coord',
                                            placeholder=0,
                                            value=0,
                                            type='number',
                                            min=0,
                                            max=0,
                                            step=1,
                                            disabled=True
                                        )
                                    ],
                                    id='x_coord_group',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'width': '95%'}
                                ),
                                width={'size': 2, 'offset': 3}
                            ),
                            dbc.Col(
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText('Y'),
                                        dbc.Input(
                                            id='y_coord',
                                            placeholder=0,
                                            value=0,
                                            type='number',
                                            min=0,
                                            max=0,
                                            step=1,
                                            disabled=True
                                        )
                                    ],
                                    id='y_coord_group',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'width': '95%'}
                                ),
                                width=2
                            ),
                            dbc.Col(
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText('Frame'),
                                        dbc.Input(
                                            id='frame',
                                            placeholder=0,
                                            value=0,
                                            type='number',
                                            min=0,
                                            max=0,
                                            step=1,
                                            disabled=True
                                        )
                                    ],
                                    id='frame_group',
                                    style={'margin': '20px',
                                           'display': 'flex',
                                           'width': '95%'}
                                ),
                                width=2
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id='spectrum',
                                    figure=blank_figure(),
                                    style={'width': '95%'}
                                ),
                                width=12
                            )
                        ]
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                dbc.ModalTitle('MALDI Metadata')

                            ),
                            dbc.ModalBody('', id='maldi_metadata_body'),
                            dbc.ModalFooter(
                                dbc.Button('Ok', id='maldi_metadata_ok_button')
                            )
                        ],
                        id='maldi_metadata_modal',
                        centered=True,
                        is_open=False
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                dbc.ModalTitle('Error')
                            ),
                            dbc.ModalBody('The selected *.d directory does not contain TSF format data.')
                        ],
                        id='load_tsf_error_modal',
                        centered=True,
                        is_open=False
                    ),
                    dcc.Store(id='store_plot'),
                    dcc.Store(id='dot_d_directory', data='')
                ],
                delay_hide=0,
                overlay_style={'visibility': 'visible', 'opacity': 0.9}
            )
        ],
        style={'margin': '20px'}
    )
    return dashboard_layout
