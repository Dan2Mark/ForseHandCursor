# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['..\PythonApplication1.py'],
             pathex=['C:\dev\PythonApplication1'],
             binaries=[],
             datas=[('FHC.ico','FHC.ico'),('Lib\site-packages/mediapipe', 'mediapipe')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

# Avoid warning
for d in a.datas:
    if '_framework_bindings.cp37-win_amd64.pyd' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ForseHandCursor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='C:\dev\PythonApplication1\FHC.ico')