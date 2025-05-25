# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all
import platform
import os

# Determine the correct architecture
is_64bit = platform.machine().endswith('64')
arch_folder = 'x64' if is_64bit else 'x86'

# Updated data files with correct paths
datas = [
    ('resources', 'resources'),
    ('drivers', 'drivers'),
    ('logo.ico', '.'),  # Add logo.ico to root
]


# Include only the correct architecture DLL
binaries = [(f'drivers/lib/{arch_folder}/libzkfpcsharp.dll', '.')]

hiddenimports = ['cv2', 'numpy', 'mediapipe', 'insightface', 'sklearn', 'skimage', 'pyzkfp', 'argon2', 'chime', 'reportlab', 'PIL', 'PySide6.QtCore', 'PySide6.QtWidgets', 'PySide6.QtGui', 'PySide6.QtCharts', 'PySide6.QtUiTools', 'pyqttoast', 'pygrabber', 'sqlite3', 'smtplib', 'email.mime.text', 'email.mime.multipart', 'email.mime.image', 'clr', 'System', 'System.IO', 'System.Reflection']

# Add additional hidden imports for .NET and Python.NET
hiddenimports += ['pythonnet', 'clr', 'System.Runtime', 'System.Runtime.InteropServices']

hiddenimports += collect_submodules('mediapipe')
hiddenimports += collect_submodules('insightface')
hiddenimports += collect_submodules('sklearn')
hiddenimports += collect_submodules('skimage')
hiddenimports += collect_submodules('onnxruntime')
hiddenimports += collect_submodules('pyzkfp')
hiddenimports += [
    'mediapipe.python._framework_bindings',
    'mediapipe.python.solutions',
    'mediapipe.python.solutions.face_mesh',
    'mediapipe.python.solutions.face_detection', 
    'mediapipe.python.solutions.hands',
    'mediapipe.python.solutions.pose',
    'mediapipe.python.solutions.holistic',
    'mediapipe.python.solutions.selfie_segmentation',
    'mediapipe.python.solutions.objectron',
    'mediapipe.python.solutions.drawing_utils',
    'mediapipe.python.solutions.drawing_styles',
    'mediapipe.tasks.python.vision',
    'google.protobuf',
    'google.protobuf.internal',
    'google.protobuf.pyext._message',
    'absl.flags',
    'absl.logging'
]

tmp_ret = collect_all('mediapipe')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('insightface')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('cv2')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('sklearn')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('skimage')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('onnxruntime')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EALS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)