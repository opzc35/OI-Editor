#!/bin/bash
# 一键打包 OI-Editor 到 Windows/Mac/Linux 可执行文件
# 需在各平台分别运行

set -e

# 1. 打包 Python 代码
pyinstaller --noconfirm --onefile --add-data "editor:editor" --add-data "ui:ui" --add-data "problems:problems" --add-data "compilers:compilers" --add-data "themes:themes" --add-data "resources:resources" main.py

# 2. 拷贝内置编译器到 dist 目录
mkdir -p dist/compilers
cp -r compiler/* dist/compilers/ || true

echo "打包完成，编译器已内置。请在 dist/ 目录下查找可执行文件。"
