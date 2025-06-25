# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'app\main.py'],
    pathex=[r'venv\Lib\site-packages'],
    binaries=[],
    datas=[
        # 数据库文件
        ('barrage.db', '.'),
        # 环境变量文件
        ('.env', '.')
    ],
    hiddenimports=[
        'app',
        'app.main',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='barrage-service',
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
    icon=r'icons\favicon.ico'
)

collect = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='barrage-service'
)