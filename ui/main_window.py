from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter, QTextBrowser, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from editor.monaco_widget import MonacoEditorWidget
from problems.problem_viewer import ProblemViewer
import openai
from PyQt6.QtWidgets import QMessageBox
import os
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QDialogButtonBox

class SettingsDialog(QDialog):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        layout = QFormLayout(self)
        self.theme_box = QComboBox()
        self.theme_box.addItems(["深色", "浅色"])
        if config and config.get('theme') == 'vs':
            self.theme_box.setCurrentIndex(1)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setText(config.get('openai_api_key', ''))
        self.api_url_edit = QLineEdit()
        self.api_url_edit.setText(config.get('openai_api_url', 'https://api.openai.com/v1'))
        self.model_edit = QLineEdit()
        self.model_edit.setText(config.get('openai_model', 'gpt-3.5-turbo'))
        layout.addRow("系统模式", self.theme_box)
        layout.addRow("OpenAI API Key", self.api_key_edit)
        layout.addRow("OpenAI API 地址", self.api_url_edit)
        layout.addRow("模型名称", self.model_edit)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_settings(self):
        return {
            'theme': 'vs' if self.theme_box.currentIndex() == 1 else 'vs-dark',
            'openai_api_key': self.api_key_edit.text(),
            'openai_api_url': self.api_url_edit.text(),
            'openai_model': self.model_edit.text()
        }

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

        # AI 翻译菜单
        ai_menu = menubar.addMenu("AI")
        translate_action = QAction("翻译当前代码", self)
        translate_action.triggered.connect(self.translate_code)
        ai_menu.addAction(translate_action)
        # 设置面板
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.open_settings)
        menubar.addAction(settings_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "All Files (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            self.editor.set_code(code)

    def translate_code(self):
        code = self.editor.webview.page().runJavaScript("editor.getValue()", lambda code: self._do_translate(code))

    def _do_translate(self, code):
        config = getattr(self, '_config', {})
        api_key = config.get('openai_api_key') or os.environ.get('OPENAI_API_KEY')
        api_url = config.get('openai_api_url', 'https://api.openai.com/v1')
        model = config.get('openai_model', 'gpt-3.5-turbo')
        if not api_key:
            QMessageBox.warning(self, "AI 错误", "请先在设置中填写 OpenAI API Key")
            return
        openai.api_key = api_key
        openai.api_base = api_url
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个代码翻译助手，请将输入的代码注释翻译为英文。"},
                    {"role": "user", "content": code}
                ]
            )
            translation = response['choices'][0]['message']['content']
        except Exception as e:
            translation = f"AI 翻译失败: {e}"
        QMessageBox.information(self, "AI 翻译结果", translation)

    def open_settings(self):
        config = getattr(self, '_config', {})
        dlg = SettingsDialog(self, config)
        if dlg.exec():
            settings = dlg.get_settings()
            self._config = settings
            # 应用主题
            self.editor.set_theme(settings['theme'])
            # 保存API设置，可扩展为持久化
            print("应用设置:", settings)

    def get_config(self):
        # 这里应该从配置文件加载设置
        return {
            'theme': 'vs-dark',
            'openai_api_key': 'sk-xxx',
            'openai_api_url': 'https://api.openai.com/v1',
            'openai_model': 'gpt-3.5-turbo'
        }

    def apply_settings(self, settings):
        # 这里应该保存设置到配置文件
        print("应用设置:", settings)
        if settings['theme'] == 'vs':
            self.editor.set_theme('vs')
        else:
            self.editor.set_theme('vs-dark')
