# TSFImagingDataViewer
TSFImagingDataViewer is a simple data visualization tool developed in Python 3.11 using Dash and pywebview to allow 
mass spectrometrists using Bruker MALDI-TOFs to visualize their raw TSF format data.

## Installation
No installation is required. Simply download TSFImagingDataViewer 
[here](https://github.com/gtluu/TSFImagingDataViewer/releases/download/v1.0.0/TSFImagingDataViewer_1.0.0.zip) and 
run TSFImagingDataViewer.exe.

## Usage
All options are disabled until a dataset is loaded. Click on the `Load Bruker *.d Dataset` button and select a *.d 
directory to load. Within the `*.d` directory, the raw data should be stored as `analysis.tsf`/`analysis.tdf_bin`. If 
these files are not found, an error message will appear.

Once loaded, several options are available for analysis.

#### Spectrum Viewer
Individual spectra for each `Frame`, which have corresponding `x` and `y` coordinates, can be viewed in the Spectrum 
Viewer. Updating the current `Frame` will update the `x` and `y` coordinates; similarly, updating coordinates will 
update the `Frame`.

The spectrum is plotted using `plotly`, which allows for zooming, viewing m/z and intensity values by hovering over a 
peak, saving snapshots as a `png` file, and any other functions native to `plotly` plots. Additionally, 
`plotly-resampler` has been implemented to allow for displaying spectra with large numbers of data points. When zooming 
in or out, you may notice the spectrum updating for a split second due to this implementation.

The average spectrum of the entire dataset can also be viewed by clicking on the `View Full Average Spectrum` button. 
WARNING: THIS PROCESS CAN BE EXTREMELY TIME CONSUMING FOR LARGER DATASETS. Instead, the 
`View Average Estimate Spectrum` button will create an average spectrum using a subset of 20% of the total number of 
spectra in the dataset. After generating the full average or average estimate spectrum, a file named 
`average_full.pickle` or `average_estimate.pickle` will be saved within the `*.d` directory. If a previous average has 
been generated when these buttons are clicked, they will instead by loaded from the `pickle` files to save time. To 
generate a new average, delete these `pickle` files.

#### Ion Image Viewer
Using the `m/z` and `m/z tolerance` boxes, ion images for a given feature can be viewed in the Ion Image Viewer. The 
`m/z` box can also be populated by clicking on a peak in the currently displayed spectrum. Clicking on 
`Update Ion image` will generate the ion image. WARNING: SIMILAR TO GENERATING THE FULL AVERAGE SPECTRUM, THIS PROCESS 
CAN BE TIME CONSUMING. For viewing multiple ion images, 
[SCiLS Lab](https://www.bruker.com/en/products-and-solutions/mass-spectrometry/ms-software/scils-lab.html) is 
recommended.
