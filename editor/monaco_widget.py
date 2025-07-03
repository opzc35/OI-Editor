from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
import os

class MonacoEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setLayout(layout)
        self.load_editor()

    def load_editor(self):
        # 加载本地Monaco Editor HTML
        editor_html = os.path.join(os.path.dirname(__file__), 'monaco.html')
        self.webview.load(f'file://{editor_html}')

    def set_code(self, code: str):
        # 通过JS设置代码内容
        js = f"window.setEditorCode({repr(code)})"
        self.webview.page().runJavaScript(js)

    def set_theme(self, theme: str):
        js = f"window.setEditorTheme('{theme}')"
        self.webview.page().runJavaScript(js)
