from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter, QTextBrowser, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from editor.monaco_widget import MonacoEditorWidget
from problems.problem_viewer import ProblemViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OI-Editor")
        self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.editor = MonacoEditorWidget()
        self.problem_viewer = ProblemViewer()

        splitter.addWidget(self.problem_viewer)
        splitter.addWidget(self.editor)
        splitter.setSizes([300, 900])

        layout.addWidget(splitter)
        self.setCentralWidget(central_widget)
        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")
        open_action = QAction("打开文件", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        theme_menu = menubar.addMenu("主题")
        dark_action = QAction("深色模式", self)
        light_action = QAction("浅色模式", self)
        dark_action.triggered.connect(lambda: self.editor.set_theme('vs-dark'))
        light_action.triggered.connect(lambda: self.editor.set_theme('vs'))
        theme_menu.addAction(dark_action)
        theme_menu.addAction(light_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "All Files (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            self.editor.set_code(code)
