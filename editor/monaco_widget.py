from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import os
import sys

class MonacoEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setLayout(layout)
        self.webview.loadFinished.connect(self.on_load_finished)
        self.load_editor()
        self._pending_code = None
        self._pending_theme = None

    def load_editor(self):
        # 加载本地Monaco Editor HTML
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                import os
                return os.path.join(sys._MEIPASS, relative_path)
            import os
            return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)
        editor_html = resource_path('editor/monaco.html')
        url = QUrl.fromLocalFile(editor_html)
        self.webview.load(url)

    def on_load_finished(self, ok):
        if ok:
            if self._pending_code is not None:
                self.set_code(self._pending_code)
                self._pending_code = None
            if self._pending_theme is not None:
                self.set_theme(self._pending_theme)
                self._pending_theme = None

    def set_code(self, code: str):
        # 通过JS设置代码内容
        js = f"window.setEditorCode({repr(code)})"
        # If the editor is not loaded yet, store the code to set later
        if not self.webview.page().url().isValid():
            self._pending_code = code
        else:
            self.webview.page().runJavaScript(js)

    def set_theme(self, theme: str):
        js = f"window.setEditorTheme('{theme}')"
        # If the editor is not loaded yet, store the theme to set later
        if not self.webview.page().url().isValid():
            self._pending_theme = theme
        else:
            self.webview.page().runJavaScript(js)
