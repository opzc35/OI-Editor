# 本脚本已不再需要下载，改为检测本地 gcc 目录结构是否完整。
# 请将各平台的 gcc/clang 可执行文件和依赖提前放入 gcc/windows/bin、gcc/linux/bin、gcc/macos/bin。
# 打包时用 PyInstaller 的 --add-data 参数一并打包。

import os
import platform

def check_gcc():
    base = os.path.abspath(os.path.dirname(__file__))
    sysname = platform.system()
    if sysname == 'Windows':
        path = os.path.join(base, 'gcc', 'windows', 'bin', 'g++.exe')
        if os.path.exists(path):
            print('Windows gcc 已内置:', path)
        else:
            print('未找到 gcc/windows/bin/g++.exe，请手动放置！')
    elif sysname == 'Linux':
        path = os.path.join(base, 'gcc', 'linux', 'bin', 'g++')
        if os.path.exists(path):
            print('Linux gcc 已内置:', path)
        else:
            print('未找到 gcc/linux/bin/g++，请手动放置！')
    elif sysname == 'Darwin':
        path = os.path.join(base, 'gcc', 'macos', 'bin', 'clang++')
        if os.path.exists(path):
            print('macOS clang++ 已内置:', path)
        else:
            print('未找到 gcc/macos/bin/clang++，请手动放置！')
    else:
        print('未知平台，请手动放置对应编译器！')

if __name__ == '__main__':
    check_gcc()
