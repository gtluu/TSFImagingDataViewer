# The following code has been modified from TIMSCONVERT, pyMALDIproc/pyMALDIviz, and flex_maldi_dda_automation.
# For more information, see the following links:
# https://github.com/gtluu/timsconvert
# https://github.com/gtluu/pymaldiproc
# https://github.com/gtluu/flex_maldi_dda_automation


import os
import copy
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly_resampler import FigureResampler
from pyTDFSDK.classes import TsfSpectrum


# Copied from TIMSCONVERT.
def schema_detection(bruker_dot_d_file):
    """
    Detect the schema used by the raw data in the Bruker .d directory.

    :param bruker_dot_d_file: Path to the .d directory of interest.
    :type: str
    :return: Capitalized schema extension (TDF, TSF, or BAF).
    :rtype: str
    """
    exts = [os.path.splitext(fname)[1] for dirpath, dirnames, filenames in os.walk(bruker_dot_d_file)
            for fname in filenames]
    if '.tdf' in exts and '.tsf' not in exts and '.baf' not in exts:
        return 'TDF'
    elif '.tsf' in exts and '.tdf' not in exts and '.baf' not in exts:
        return 'TSF'
    elif '.baf' in exts and '.tdf' not in exts and '.tsf' not in exts:
        return 'BAF'


def get_ppm_tolerance(mz, ppm):
    """
    Get the tolerance in Daltons for a given m/z value at N ppm.

    :param mz: m/z value
    :type mz: float
    :param ppm: ppm tolerance
    :type ppm: int | float
    :return: Tolerance in Daltons
    :rtype: float
    """
    return ppm * (mz / (10**6))


# Copied from pyMALDIproc.
def trim_spectrum(mz_array, intensity_array, lower_mass_range, upper_mass_range):
    """
       Trim the mass spectrum to only include features between the user specified lower and upper mass ranges
       (inclusive).

       :param mz_array: Numpy array containing m/z values.
       :type mz_array: numpy.array
       :param intensity_array: Numpy array containing intensity values.
       :type intensity_array: numpy.array
       :param lower_mass_range: Mass in daltons to use for the lower mass range.
       :type lower_mass_range: int
       :param upper_mass_range: Mass in Daltons to use for the upper mass range.
       :type upper_mass_range: int
       """
    indices = np.where((mz_array >= lower_mass_range) & (mz_array <= upper_mass_range))[0]
    mz_array = copy.deepcopy(mz_array[indices])
    intensity_array = copy.deepcopy(intensity_array[indices])
    return mz_array, intensity_array


def create_average_spectrum(data, frame_ids, full=False):
    """
    Create an average spectrum from a TsfData dataset for a list of frames.

    :param data: TSF dataset.
    :type data: pyTDFSDK.classes.TsfData
    :param frame_ids: List of frame IDs to average.
    :type frame_ids: list[int]
    :param full: Whether the average being calculated is a full or average spectrum.
    :type full: bool
    :return: Numpy array containing average intensity values.
    :rtype: numpy.array
    """
    intensity_array = np.array([])
    for i in frame_ids:
        spectrum = TsfSpectrum(data, frame=i, mode='profile')
        if intensity_array.size == 0:
            intensity_array = spectrum.intensity_array
            mz_array = spectrum.mz_array  # assume m/z axis for profile data is the same
        else:
            intensity_array = np.sum([intensity_array, spectrum.intensity_array], axis=0)
    intensity_array = intensity_array / len(frame_ids)
    return mz_array, intensity_array


# Copied for pyMALDIviz.
def blank_figure():
    """
    Obtain a blank figure wrapped by plotly_resampler.FigureResampler to be used as a placeholder.

    :return: Blank figure.
    """
    fig = FigureResampler(go.Figure(go.Scatter(x=[], y=[])))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


# Copied for pyMALDIviz.
def get_spectrum(spectrum):
    """
    Plot the spectrum to a plotly.express.line plot wrapped by plotly_resampler.FigureResampler.

    :param spectrum: Spectrum object whose data is used to generate the figure.
    :type spectrum: pyTDFSDK.classes.TsfSpectrum
    :return: Plotly figure containing mass spectrum.
    """
    spectrum_df = pd.DataFrame({'m/z': copy.deepcopy(spectrum.mz_array),
                                'Intensity': copy.deepcopy(spectrum.intensity_array)})
    fig = FigureResampler(px.line(data_frame=spectrum_df,
                                  x='m/z',
                                  y='Intensity',
                                  hover_data={'m/z': ':.4f',
                                              'Intensity': ':.1f'}))
    fig.update_layout(xaxis_tickformat='d',
                      yaxis_tickformat='~e')
    return fig


def get_spectrum_from_arrays(spectrum_df):
    """
    Plot the spectrum to a plotly.express.line plot wrapped by plotly_resampler.FigureResampler.

    :param spectrum_df: Spectrum dataframe containing columns 'm/z' and 'Intensity'.
    :type spectrum_df: pandas.DataFrame
    :return: Plotly figure containing mass spectrum.
    """
    fig = FigureResampler(px.line(data_frame=spectrum_df,
                                  x='m/z',
                                  y='Intensity',
                                  hover_data={'m/z': ':.4f',
                                              'Intensity': ':.1f'}))
    fig.update_layout(xaxis_tickformat='d',
                      yaxis_tickformat='~e')
    return fig


def get_ion_image(data, mz, mz_tolerance, mz_tolerance_unit):
    """
    Plot the ion image to a plotly.express.imshow plot.

    :param data: TSF dataset loaded by pyTDFSDK.
    :type data: pyTDFSDK.classes.TsfData
    :param mz: m/z value of interest.
    :type mz: float
    :param mz_tolerance: m/z tolerance to be used (+/-).
    :type mz_tolerance: float
    :param mz_tolerance_unit: Whether the m/z tolerance is in Da or ppm. If not specified, the default tolerance is 0.
    :type mz_tolerance_unit: str
    :return: Plotly figure containing ion image.
    """
    if mz_tolerance_unit == 'Da':
        tolerance = mz_tolerance
    elif mz_tolerance_unit == 'ppm':
        tolerance = get_ppm_tolerance(mz, mz_tolerance)
    else:
        tolerance = 0

    lower_mass_range = mz - tolerance
    upper_mass_range = mz + tolerance
    mz_min = float(data.analysis['GlobalMetadata']['MzAcqRangeLower'])
    mz_max = float(data.analysis['GlobalMetadata']['MzAcqRangeUpper'])
    if lower_mass_range < mz_min:
        lower_mass_range = mz_min
    if upper_mass_range > mz_max:
        upper_mass_range = mz_max
    min_x = int(data.analysis['GlobalMetadata']['ImagingAreaMinXIndexPos'])
    max_x = int(data.analysis['GlobalMetadata']['ImagingAreaMaxXIndexPos'])
    min_y = int(data.analysis['GlobalMetadata']['ImagingAreaMinYIndexPos'])
    max_y = int(data.analysis['GlobalMetadata']['ImagingAreaMaxYIndexPos'])

    frame_ids = data.analysis['Frames']['Id'].values
    list_of_scan_dicts = []
    for i in frame_ids:
        spectrum = TsfSpectrum(data, frame=i, mode='profile')
        mz_array, intensity_array = trim_spectrum(spectrum.mz_array,
                                                  spectrum.intensity_array,
                                                  lower_mass_range,
                                                  upper_mass_range)
        list_of_scan_dicts.append({'intensity': np.sum(intensity_array),
                                   'x_coord': spectrum.coord[0],
                                   'y_coord': spectrum.coord[1]})
    intensity_df = pd.DataFrame(list_of_scan_dicts)
    intensity_df['x_coord'] = intensity_df['x_coord'] - min_x
    intensity_df['y_coord'] = intensity_df['y_coord'] - min_y
    if np.sum(intensity_df['intensity']) == 0:
        upper_range_color = 1
    else:
        upper_range_color = None
    ion_image_array = pd.merge(intensity_df,
                               pd.DataFrame([{'x_coord': i, 'y_coord': j}
                                             for i in np.arange(0, max_x - min_x + 1, 1)
                                             for j in np.arange(0, max_y - min_y + 1, 1)]),
                               how='outer',
                               on=['x_coord', 'y_coord']).fillna(value=0).pivot(index='y_coord',
                                                                                columns='x_coord',
                                                                                values='intensity').fillna(value=0)
    ion_image = px.imshow(ion_image_array.values, color_continuous_scale='viridis', range_color=[0, upper_range_color])
    ion_image.update_xaxes(showticklabels=False)
    ion_image.update_yaxes(showticklabels=False)
    return ion_image
