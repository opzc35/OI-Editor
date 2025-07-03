# OI-Editor

OI-Editor 是一个基于 PyQt6 和 Monaco Editor 的多语言编程编辑器，支持 Python、C++、Java、Pascal 的编译与运行，内置编译器，无需用户额外安装。

## 主要特性
- Monaco 编辑器美化，支持深色/浅色模式
- 支持 Python、C++、Java、Pascal 编译与运行
- 内置题目查看器
- 跨平台

## 运行方式
```bash
pip install -r requirements.txt
python main.py
```

## 目录结构
- `main.py`：程序入口
- `editor/`：编辑器相关代码
- `compilers/`：编译器相关代码
- `ui/`：界面相关代码
- `problems/`：题目查看器
- `themes/`：主题配置
- `resources/`：资源文件
