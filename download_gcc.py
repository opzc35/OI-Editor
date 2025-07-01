import os
import sys
import platform
import urllib.request
import zipfile
import tarfile

def download_and_extract(url, extract_to, is_zip=True, member_filter=None):
    filename = url.split('/')[-1]
    print(f"Downloading {url} ...")
    urllib.request.urlretrieve(url, filename)
    print(f"Extracting {filename} ...")
    if is_zip:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    else:
        with tarfile.open(filename, 'r:*') as tar_ref:
            if member_filter:
                members = [m for m in tar_ref.getmembers() if member_filter(m)]
                tar_ref.extractall(extract_to, members=members)
            else:
                tar_ref.extractall(extract_to)
    os.remove(filename)

# Windows: MinGW-w64 portable
win_url = "https://github.com/niXman/mingw-builds-binaries/releases/download/13.2.0-rt_v11-rev0/x86_64-13.2.0-release-win32-seh-ucrt-rt_v11-rev0.7z"
# Linux: musl-gcc static (示例, 你可换成 tcc 或其它小型编译器)
linux_url = "https://musl.cc/x86_64-linux-musl-cross.tgz"
# macOS: tcc (TinyCC, 体积小, 仅供演示, 你可换成 llvm)
macos_url = "https://download.savannah.nongnu.org/releases/tinycc/tcc-0.9.27.tar.bz2"

os.makedirs('gcc/windows/bin', exist_ok=True)
os.makedirs('gcc/linux/bin', exist_ok=True)
os.makedirs('gcc/macos/bin', exist_ok=True)

# Windows: 7z 解压需本地有 7z
if platform.system() == 'Windows':
    import subprocess
    print("下载并解压 Windows MinGW-w64 ...")
    urllib.request.urlretrieve(win_url, 'mingw.7z')
    subprocess.run(['7z', 'x', 'mingw.7z', f'-ogcc/windows'], check=True)
    os.remove('mingw.7z')
    print("请将 gcc/windows/bin 添加到你的打包路径")

# Linux
print("下载并解压 Linux musl-gcc ...")
download_and_extract(linux_url, 'gcc/linux', is_zip=False)
print("请将 gcc/linux/bin 添加到你的打包路径")

# macOS
print("下载并解压 macOS tcc ...")
download_and_extract(macos_url, 'gcc/macos', is_zip=False)
print("请将 gcc/macos/bin 添加到你的打包路径")

print("全部平台编译器下载完成！")
