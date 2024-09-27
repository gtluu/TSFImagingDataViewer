# The following code has been modified from pyMALDIproc/pyMALDIviz and flex_maldi_dda_automation.
# For more information, see the following links:
# https://github.com/gtluu/pymaldiproc
# https://github.com/gtluu/flex_maldi_dda_automation


import os
import copy
import numpy as np
import pandas as pd
from dash import State, callback_context, no_update
import dash_bootstrap_components as dbc
from dash_extensions.enrich import (Input, Output, DashProxy, MultiplexerTransform, Serverside,
                                    ServersideOutputTransform, FileSystemBackend)
import plotly.express as px
from plotly_resampler import FigureResampler
import tempfile
import tkinter
from tkinter.filedialog import askdirectory
from pyTDFSDK.classes import TsfData, TsfSpectrum
from pyTDFSDK.init_tdf_sdk import init_tdf_sdk_api
from TSFImagingDataViewer.layout import get_dashboard_layout
from TSFImagingDataViewer.util import (schema_detection, get_spectrum, get_spectrum_from_arrays, get_ion_image,
                                       create_average_spectrum)

FILE_SYSTEM_BACKEND = tempfile.TemporaryDirectory().name
DATA = None

app = DashProxy(prevent_initial_callbacks=True,
                transforms=[MultiplexerTransform(),
                            ServersideOutputTransform(backends=[FileSystemBackend(cache_dir=FILE_SYSTEM_BACKEND)])],
                external_stylesheets=[dbc.themes.SPACELAB])
app.layout = get_dashboard_layout()


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('ion_image', 'figure'),
               Output('mz', 'value'),
               Output('mz', 'min'),
               Output('mz', 'max'),
               Output('x_coord', 'value'),
               Output('x_coord', 'min'),
               Output('x_coord', 'max'),
               Output('y_coord', 'value'),
               Output('y_coord', 'min'),
               Output('y_coord', 'max'),
               Output('frame', 'value'),
               Output('frame', 'min'),
               Output('frame', 'max'),
               Output('average_estimate', 'disabled'),
               Output('average_full', 'disabled'),
               Output('per_frame', 'disabled'),
               Output('mz', 'disabled'),
               Output('mz_tolerance', 'disabled'),
               Output('mz_tolerance_unit', 'disabled'),
               Output('update_ion_image', 'disabled'),
               Output('x_coord', 'disabled'),
               Output('y_coord', 'disabled'),
               Output('frame', 'disabled'),
               Output('dot_d_directory', 'data'),
               Output('load_tsf_error_modal', 'is_open')],
              Input('load_tsf', 'n_clicks'))
def upload_data(n_clicks):
    changed_id = [i['prop_id'] for i in callback_context.triggered][0]
    if changed_id == 'load_tsf.n_clicks':
        global DATA
        main_tk_window = tkinter.Tk()
        main_tk_window.attributes('-topmost', True, '-alpha', 0)
        dot_d_directory = askdirectory(mustexist=True)
        main_tk_window.destroy()
        if dot_d_directory.endswith('.d') and schema_detection(dot_d_directory) == 'TSF':
            DATA = TsfData(dot_d_directory, init_tdf_sdk_api())
            spectrum = TsfSpectrum(DATA, frame=1, mode='profile')
            fig = get_spectrum(spectrum)
            ion_image = px.imshow(np.zeros((2, 2)), color_continuous_scale='viridis', range_color=[0, 1])
            maldiframeinfo_dict = DATA.analysis['MaldiFrameInfo'][DATA.analysis['MaldiFrameInfo']['Frame'] ==
                                                                  1].to_dict(orient='records')[0]
            mz_value = float(DATA.analysis['GlobalMetadata']['MzAcqRangeLower'])
            mz_min = float(DATA.analysis['GlobalMetadata']['MzAcqRangeLower'])
            mz_max = float(DATA.analysis['GlobalMetadata']['MzAcqRangeUpper'])
            x_value = int(maldiframeinfo_dict['XIndexPos'])
            x_min = int(DATA.analysis['GlobalMetadata']['ImagingAreaMinXIndexPos'])
            x_max = int(DATA.analysis['GlobalMetadata']['ImagingAreaMaxXIndexPos'])
            y_value = int(maldiframeinfo_dict['YIndexPos'])
            y_min = int(DATA.analysis['GlobalMetadata']['ImagingAreaMinYIndexPos'])
            y_max = int(DATA.analysis['GlobalMetadata']['ImagingAreaMaxYIndexPos'])
            frame_value = 1
            frame_min = int(np.min(DATA.analysis['Frames']['Id'].values))
            frame_max = int(np.max(DATA.analysis['Frames']['Id'].values))
            return (fig, Serverside(fig), ion_image,
                    mz_value, mz_min, mz_max,
                    x_value, x_min, x_max, y_value, y_min, y_max,
                    frame_value, frame_min, frame_max,
                    False, False, False, False, False, False, False, False, False, False,
                    dot_d_directory, False)
        else:
            return no_update
    else:
        return no_update


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('x_coord_group', 'style'),
               Output('y_coord_group', 'style'),
               Output('frame_group', 'style')],
              Input('average_estimate', 'n_clicks'),
              [State('x_coord_group', 'style'),
               State('y_coord_group', 'style'),
               State('frame_group', 'style')])
def show_average_estimate(n_clicks, x_coord_group_style, y_coord_group_style, frame_group_style):
    changed_id = [i['prop_id'] for i in callback_context.triggered][0]
    if changed_id == 'average_estimate.n_clicks':
        global DATA
        if os.path.isfile(os.path.join(DATA.source_file, 'average_estimate.pickle')):
            spectrum_df = pd.read_pickle(os.path.join(DATA.source_file, 'average_estimate.pickle'))
        else:
            frame_ids = DATA.analysis['Frames']['Id'].values
            frame_ids = frame_ids[::int(frame_ids.size / (frame_ids.size * 0.2))]
            mz_array, intensity_array = create_average_spectrum(DATA, frame_ids)
            spectrum_df = pd.DataFrame({'m/z': copy.deepcopy(mz_array),
                                        'Intensity': copy.deepcopy(intensity_array)})
            spectrum_df.to_pickle(os.path.join(DATA.source_file, 'average_estimate.pickle'))
        fig = get_spectrum_from_arrays(spectrum_df)
        x_coord_group_style['display'] = 'none'
        y_coord_group_style['display'] = 'none'
        frame_group_style['display'] = 'none'
        return fig, Serverside(fig), x_coord_group_style, y_coord_group_style, frame_group_style
    else:
        return no_update


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('x_coord_group', 'style'),
               Output('y_coord_group', 'style'),
               Output('frame_group', 'style')],
              Input('average_full', 'n_clicks'),
              [State('x_coord_group', 'style'),
               State('y_coord_group', 'style'),
               State('frame_group', 'style')])
def show_average_full(n_clicks, x_coord_group_style, y_coord_group_style, frame_group_style):
    changed_id = [i['prop_id'] for i in callback_context.triggered][0]
    if changed_id == 'average_full.n_clicks':
        global DATA
        if os.path.isfile(os.path.join(DATA.source_file, 'average_full.pickle')):
            spectrum_df = pd.read_pickle(os.path.join(DATA.source_file, 'average_full.pickle'))
        else:
            frame_ids = DATA.analysis['Frames']['Id'].values

            mz_array, intensity_array = create_average_spectrum(DATA, frame_ids)
            spectrum_df = pd.DataFrame({'m/z': copy.deepcopy(mz_array),
                                        'Intensity': copy.deepcopy(intensity_array)})
            spectrum_df.to_pickle(os.path.join(DATA.source_file, 'average_full.pickle'))
        fig = get_spectrum_from_arrays(spectrum_df)
        x_coord_group_style['display'] = 'none'
        y_coord_group_style['display'] = 'none'
        frame_group_style['display'] = 'none'
        return fig, Serverside(fig), x_coord_group_style, y_coord_group_style, frame_group_style
    else:
        return no_update


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('x_coord_group', 'style'),
               Output('y_coord_group', 'style'),
               Output('frame_group', 'style')],
              Input('per_frame', 'n_clicks'),
              [State('frame', 'value'),
               State('x_coord_group', 'style'),
               State('y_coord_group', 'style'),
               State('frame_group', 'style')])
def view_per_frame_spectra(n_clicks, frame,
                           x_coord_group_style, y_coord_group_style, frame_group_style):
    changed_id = [i['prop_id'] for i in callback_context.triggered][0]
    if changed_id == 'per_frame.n_clicks':
        if frame == 0:
            frame = 1
        global DATA
        spectrum = TsfSpectrum(DATA, frame=frame, mode='profile')
        fig = get_spectrum(spectrum)
        x_coord_group_style['display'] = 'flex'
        y_coord_group_style['display'] = 'flex'
        frame_group_style['display'] = 'flex'
        return fig, Serverside(fig), x_coord_group_style, y_coord_group_style, frame_group_style
    else:
        return no_update


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('x_coord', 'value'),
               Output('y_coord', 'value')],
              Input('frame', 'value'))
def update_spectrum_from_frame(frame):
    changed_id = callback_context
    if changed_id.triggered[0]['prop_id'].split('.')[0] == 'frame':
        global DATA
        spectrum = TsfSpectrum(DATA, frame=frame, mode='profile')
        fig = get_spectrum(spectrum)
        maldiframeinfo_dict = DATA.analysis['MaldiFrameInfo'][DATA.analysis['MaldiFrameInfo']['Frame'] ==
                                                              frame].to_dict(orient='records')[0]
        return fig, Serverside(fig), int(maldiframeinfo_dict['XIndexPos']), int(maldiframeinfo_dict['YIndexPos'])
    else:
        return no_update


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('frame', 'value')],
              Input('x_coord', 'value'),
              State('y_coord', 'value'))
def update_spectrum_from_x_coord(x_coord, y_coord):
    changed_id = callback_context
    if changed_id.triggered[0]['prop_id'].split('.')[0] == 'x_coord':
        global DATA
        maldiframeinfo_dict = \
            DATA.analysis['MaldiFrameInfo'][(DATA.analysis['MaldiFrameInfo']['XIndexPos'] == x_coord) &
                                            (DATA.analysis['MaldiFrameInfo']['YIndexPos'] == y_coord)].to_dict(
                orient='records')[0]
        spectrum = TsfSpectrum(DATA, frame=maldiframeinfo_dict['Frame'], mode='profile')
        fig = get_spectrum(spectrum)
        return fig, Serverside(fig), maldiframeinfo_dict['Frame']
    else:
        return no_update


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('frame', 'value')],
              Input('y_coord', 'value'),
              State('x_coord', 'value'))
def update_spectrum_from_y_coord(y_coord, x_coord):
    changed_id = callback_context
    if changed_id.triggered[0]['prop_id'].split('.')[0] == 'y_coord':
        global DATA
        maldiframeinfo_dict = \
            DATA.analysis['MaldiFrameInfo'][(DATA.analysis['MaldiFrameInfo']['XIndexPos'] == x_coord) &
                                            (DATA.analysis['MaldiFrameInfo']['YIndexPos'] == y_coord)].to_dict(
                orient='records')[0]
        spectrum = TsfSpectrum(DATA, frame=maldiframeinfo_dict['Frame'], mode='profile')
        fig = get_spectrum(spectrum)
        return fig, Serverside(fig), maldiframeinfo_dict['Frame']
    else:
        return no_update


@app.callback(Output('ion_image', 'figure'),
              Input('update_ion_image', 'n_clicks'),
              [State('mz', 'value'),
               State('mz_tolerance', 'value'),
               State('mz_tolerance_unit', 'value')])
def update_ion_image(n_clicks, mz, mz_tolerance, mz_tolerance_unit):
    changed_id = [i['prop_id'] for i in callback_context.triggered][0]
    if changed_id == 'update_ion_image.n_clicks':
        global DATA
        ion_image = get_ion_image(DATA, mz, mz_tolerance, mz_tolerance_unit)
        return ion_image
    else:
        return no_update


@app.callback(Output('mz', 'value'),
              Input('spectrum', 'clickData'))
def update_mz_from_spectrum(peak):
    changed_id = [i['prop_id'] for i in callback_context.triggered][0]
    if changed_id == 'spectrum.clickData':
        global DATA
        mz = round(peak['points'][0]['x'], 4)
        return mz


@app.callback([Output('spectrum', 'figure'),
               Output('store_plot', 'data'),
               Output('x_coord', 'value'),
               Output('y_coord', 'value'),
               Output('frame', 'value')],
              Input('ion_image', 'clickData'))
def update_spectrum_from_ion_image(coords):
    changed_id = [i['prop_id'] for i in callback_context.triggered][0]
    if changed_id == 'ion_image.clickData':
        global DATA
        x_coord = int(coords['points'][0]['x']) + int(DATA.analysis['GlobalMetadata']['ImagingAreaMinXIndexPos'])
        y_coord = int(coords['points'][0]['y']) + int(DATA.analysis['GlobalMetadata']['ImagingAreaMinYIndexPos'])
        maldiframeinfo_dict = \
            DATA.analysis['MaldiFrameInfo'][(DATA.analysis['MaldiFrameInfo']['XIndexPos'] == x_coord) &
                                            (DATA.analysis['MaldiFrameInfo']['YIndexPos'] == y_coord)].to_dict(
                orient='records')[0]
        spectrum = TsfSpectrum(DATA, frame=maldiframeinfo_dict['Frame'], mode='profile')
        fig = get_spectrum(spectrum)
        return fig, Serverside(fig), x_coord, y_coord, maldiframeinfo_dict['Frame']


@app.callback(Output('spectrum', 'figure', allow_duplicate=True),
              Input('spectrum', 'relayoutData'),
              State('store_plot', 'data'),
              prevent_initial_call=True,
              memoize=True)
def resample_spectrum(relayoutdata: dict, fig: FigureResampler):
    """
    Dash callback used for spectrum resampling to improve plotly figure performance.

    :param relayoutdata: Input signal with dictionary with spectrum_plot relayoutData.
    :param fig: State signal for data store for plotly_resampler.
    :return: Figure object used to update spectrum_plot figure.
    """
    if fig is None:
        return no_update
    return fig.construct_update_data_patch(relayoutdata)


if __name__ == '__main__':
    app.run_server(debug=False)
