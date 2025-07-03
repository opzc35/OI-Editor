#!/bin/bash
# 一键打包 OI-Editor 到 Windows/Mac/Linux 可执行文件
# 需在各平台分别运行

set -e

# 下载 Monaco Editor release 包
MONACO_VERSION=0.44.0
MONACO_URL="https://github.com/microsoft/monaco-editor/releases/download/v$MONACO_VERSION/monaco-editor-$MONACO_VERSION.zip"
MONACO_TMP=monaco_tmp
MONACO_DIR=editor/monaco

if [ ! -d "$MONACO_DIR/min/vs" ]; then
    echo "Downloading Monaco Editor..."
    mkdir -p $MONACO_TMP
    curl -L "$MONACO_URL" -o $MONACO_TMP/monaco.zip
    unzip -q $MONACO_TMP/monaco.zip -d $MONACO_TMP
    mkdir -p $MONACO_DIR
    cp -r $MONACO_TMP/monaco-editor-$MONACO_VERSION/min $MONACO_DIR/
    cp $MONACO_TMP/monaco-editor-$MONACO_VERSION/loader.js $MONACO_DIR/
    rm -rf $MONACO_TMP
fi

# 1. 打包 Python 代码
pyinstaller --noconfirm --onefile --add-data "editor:editor" --add-data "ui:ui" --add-data "problems:problems" --add-data "compilers:compilers" --add-data "themes:themes" --add-data "resources:resources" main.py

# 2. 拷贝内置编译器到 dist 目录（区分平台）
if [[ "$(uname -s)" == *NT* || "$(uname -o 2>/dev/null)" == *Msys* ]]; then
    # Windows 平台
    powershell -Command "if (Test-Path 'resources/compilers') { Copy-Item -Recurse -Force resources/compilers dist/resources/compilers }"
else
    # Linux/Mac 平台
    mkdir -p dist/resources/compilers
    cp -r resources/compilers/* dist/resources/compilers/ || true
fi

echo "打包完成，编译器已内置。请在 dist/ 目录下查找可执行文件。"
