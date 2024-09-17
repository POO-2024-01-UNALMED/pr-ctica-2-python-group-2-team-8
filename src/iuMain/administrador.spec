# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['administrador.py'],
    pathex=['C:/Users/juanj/OneDrive/Ingeniería de Sistemas/PYTHON/pr-ctica-2-python-group-2-team-8/src'],
    binaries=[],
    datas=[],
    hiddenimports=[

    ],
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
    name='administrador',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
