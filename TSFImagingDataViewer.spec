# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TSFImagingDataViewer.py'],
    pathex=[],
    binaries=[],
    datas=[
		('C:\\Users\\bass\\.conda\\envs\\tsfviewer\\Lib\\site-packages\\dash', 'dash'),
		('C:\\Users\\bass\\.conda\\envs\\tsfviewer\\Lib\\site-packages\\dash_bootstrap_components', 'dash_bootstrap_components'),
		('C:\\Users\\bass\\.conda\\envs\\tsfviewer\\Lib\\site-packages\\dash_core_components', 'dash_core_components'),
		('C:\\Users\\bass\\.conda\\envs\\tsfviewer\\Lib\\site-packages\\dash_extensions', 'dash_extensions'),
		('C:\\Users\\bass\\.conda\\envs\\tsfviewer\\Lib\\site-packages\\dash_html_components', 'dash_html_components'),
		('LICENSE.md', '.'),
		('README.md', '.'),
		('third-party-licenses.txt', '.'),
		('C:\\Users\\bass\\.conda\\envs\\tsfviewer\\Lib\\site-packages\\TDF-SDK', 'TDF-SDK')
	],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TSFImagingDataViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TSFImagingDataViewer',
)
