# 打包说明

- 使用 PyInstaller 打包：
  - Windows 下需准备 MinGW-w64、fpc 等编译器二进制，放入 `resources/compilers/windows/`
  - Mac 下需准备 clang/g++, fpc，放入 `resources/compilers/mac/`
  - Linux 下需准备 g++, fpc，放入 `resources/compilers/linux/`
- 运行 `build/build_all.sh`，会自动将编译器复制到最终包内。
- 用户无需额外安装编译器。

## 依赖
- PyInstaller
- 各平台编译器二进制

## 示例
```bash
bash build/build_all.sh
```
