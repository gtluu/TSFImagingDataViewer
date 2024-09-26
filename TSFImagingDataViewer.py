# The following code has been modified from pyMALDIproc/pyMALDIviz and flex_maldi_dda_automation.
# For more information, see the following links:
# https://github.com/gtluu/pymaldiproc
# https://github.com/gtluu/flex_maldi_dda_automation


import os
from contextlib import redirect_stdout
from io import StringIO
import atexit
import shutil
import webview
from TSFImagingDataViewer import VERSION
from TSFImagingDataViewer.dashboard import app, FILE_SYSTEM_BACKEND


def main():
    stream = StringIO()
    with redirect_stdout(stream):
        webview.settings['ALLOW_DOWNLOADS'] = True
        app.server.config['THREADED'] = False
        window = webview.create_window(f'TSFImagingDataViewer {VERSION}', app.server)
        webview.start()


def delete_file_system_backend():
    if os.path.exists(FILE_SYSTEM_BACKEND):
        shutil.rmtree(FILE_SYSTEM_BACKEND)


atexit.register(delete_file_system_backend)


if __name__ == '__main__':
    main()
