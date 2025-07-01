import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPlainTextEdit, QVBoxLayout, QWidget, QToolBar, QMessageBox, QStatusBar
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QProcess

class CppEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C++ 编辑器")
        self.setGeometry(200, 100, 900, 600)
        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)
        self.current_file = None
        self.process = QProcess(self)
        self.init_ui()

    def init_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        compile_action = QAction("编译", self)
        compile_action.triggered.connect(self.compile_cpp)
        toolbar.addAction(compile_action)

        run_action = QAction("运行", self)
        run_action.triggered.connect(self.run_cpp)
        toolbar.addAction(run_action)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "打开C++文件", "", "C++ Files (*.cpp *.h)")
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                self.editor.setPlainText(f.read())
            self.current_file = file
            self.status.showMessage(f"已打开: {file}")

    def save_file(self):
        if not self.current_file:
            file, _ = QFileDialog.getSaveFileName(self, "保存C++文件", "", "C++ Files (*.cpp *.h)")
            if not file:
                return
            self.current_file = file
        with open(self.current_file, 'w', encoding='utf-8') as f:
            f.write(self.editor.toPlainText())
        self.status.showMessage(f"已保存: {self.current_file}")

    def compile_cpp(self):
        if not self.current_file:
            self.save_file()
        if not self.current_file:
            return
        exe_file = os.path.splitext(self.current_file)[0]
        compile_cmd = f"g++ '{self.current_file}' -o '{exe_file}'"
        self.process.finished.connect(lambda: self.status.showMessage("编译完成"))
        self.process.start("bash", ["-c", compile_cmd])
        self.status.showMessage("正在编译...")

    def run_cpp(self):
        if not self.current_file:
            return
        exe_file = os.path.splitext(self.current_file)[0]
        if not os.path.exists(exe_file):
            QMessageBox.warning(self, "错误", "请先编译程序！")
            return
        self.process.finished.connect(lambda: self.status.showMessage("运行结束"))
        self.process.start(exe_file)
        self.status.showMessage("正在运行...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CppEditor()
    window.show()
    sys.exit(app.exec())
