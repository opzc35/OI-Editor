import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
import shutil

def download_file(url, filename):
    print(f"Downloading {url} ...")
    urllib.request.urlretrieve(url, filename)
    print(f"Saved as {filename}")

def extract_zip(filename, extract_to):
    print(f"Extracting {filename} ...")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")

def extract_tar(filename, extract_to):
    print(f"Extracting {filename} ...")
    with tarfile.open(filename, 'r:*') as tar_ref:
        tar_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")

def main():
    # 1. 下载 OI-Editor 源码
    editor_url = "https://github.com/opzc35/OI-Editor/archive/refs/heads/main.zip"
    editor_zip = "OI-Editor-main.zip"
    download_file(editor_url, editor_zip)
    extract_zip(editor_zip, ".")
    os.remove(editor_zip)
    # 移动源码到 oi-editor 目录
    if os.path.exists("oi-editor"):
        shutil.rmtree("oi-editor")
    os.rename("OI-Editor-main", "oi-editor")

    # 2. 下载并解压 gcc/clang
    sysname = platform.system()
    os.makedirs('oi-editor/gcc', exist_ok=True)
    if sysname == 'Windows':
        win_url = "https://github.com/niXman/mingw-builds-binaries/releases/download/13.2.0-rt_v11-rev0/x86_64-13.2.0-release-win32-seh-ucrt-rt_v11-rev0.7z"
        print("请确保已安装 7z 命令行工具 (https://www.7-zip.org/download.html)")
        download_file(win_url, 'mingw.7z')
        os.makedirs('oi-editor/gcc/windows', exist_ok=True)
        os.system('7z x mingw.7z -ooi-editor/gcc/windows')
        os.remove('mingw.7z')
    elif sysname == 'Linux':
        linux_url = "https://musl.cc/x86_64-linux-musl-cross.tgz"
        download_file(linux_url, 'musl-gcc.tgz')
        os.makedirs('oi-editor/gcc/linux', exist_ok=True)
        extract_tar('musl-gcc.tgz', 'oi-editor/gcc/linux')
        os.remove('musl-gcc.tgz')
    elif sysname == 'Darwin':
        macos_url = "https://download.savannah.nongnu.org/releases/tinycc/tcc-0.9.27.tar.bz2"
        download_file(macos_url, 'tcc-macos.tar.bz2')
        os.makedirs('oi-editor/gcc/macos', exist_ok=True)
        extract_tar('tcc-macos.tar.bz2', 'oi-editor/gcc/macos')
        os.remove('tcc-macos.tar.bz2')
    else:
        print("暂不支持该平台！")
        sys.exit(1)

    print("\n安装完成！请进入 oi-editor 目录，运行 main.py 启动编辑器。\n")

if __name__ == "__main__":
    main()
