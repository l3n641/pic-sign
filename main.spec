# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 1. Analysis：负责分析代码的依赖关系（找本尊和狐朋狗友）
a = Analysis(
    ['main.py'],                  # 要打包的主入口脚本
    pathex=['.'],                    # 额外的模块搜索路径
    binaries=[],                  # 需要包含 damage 的二进制文件（如 .dll, .so）
    datas=[],                     # 核心！需要打包的静态资源（如 [('src/images', 'images')]）
   hiddenimports=['views', 'views.main_view'],      # 显式指定命令行没检测出来的隐式导入
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],                  # 排除不需要的库（比如不小心装上的 pandas，可以排除掉瘦身）
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 2. PYZ：把所有 Python 脚本压缩成一个 PYZ 压缩包
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 3. EXE：负责生成最终的 exe 可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,                      # 把 Analysis 收集到的数据合并进来
    [],
    name='main',                  # 生成的 exe 文件名 (main.exe)
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                     # 是否使用 UPX 压缩降低体积
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                 # 是否保留黑色的命令行窗口 (PySide6 正式发布时通常设为 False)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[],            # 软件的图标路径
)