from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QMessageBox
import requests
from bs4 import BeautifulSoup

class ProblemViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入题目链接（支持 AtCoder, Codeforces, Luogu, Vjudge）")
        self.fetch_btn = QPushButton("获取题目")
        self.fetch_btn.clicked.connect(self.fetch_problem)
        self.browser = QTextBrowser()
        layout.addWidget(self.url_input)
        layout.addWidget(self.fetch_btn)
        layout.addWidget(self.browser)
        self.setLayout(layout)
        self.set_problem("欢迎使用 OI-Editor！\n\n请在此处查看题目内容。")

    def set_problem(self, text: str):
        self.browser.setText(text)

    def fetch_problem(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "错误", "请输入题目链接！")
            return
        try:
            if "atcoder.jp" in url:
                text = self.fetch_atcoder(url)
            elif "codeforces.com" in url:
                text = self.fetch_codeforces(url)
            elif "luogu.com.cn" in url:
                text = self.fetch_luogu(url)
            elif "vjudge.net" in url:
                text = self.fetch_vjudge(url)
            else:
                text = "暂不支持该平台。"
            self.set_problem(text)
        except Exception as e:
            QMessageBox.critical(self, "获取失败", str(e))

    def fetch_atcoder(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.find('span', class_='h2').text if soup.find('span', class_='h2') else ''
        statement = soup.find('div', class_='part').text if soup.find('div', class_='part') else ''
        return f"{title}\n\n{statement}"

    def fetch_codeforces(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.find('div', class_='title').text if soup.find('div', class_='title') else ''
        statement = soup.find('div', class_='problem-statement').text if soup.find('div', class_='problem-statement') else ''
        return f"{title}\n\n{statement}"

    def fetch_luogu(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.find('h1').text if soup.find('h1') else ''
        statement = soup.find('div', class_='main-content').text if soup.find('div', class_='main-content') else ''
        return f"{title}\n\n{statement}"

    def fetch_vjudge(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.find('h2').text if soup.find('h2') else ''
        statement = soup.find('div', class_='panel-body').text if soup.find('div', class_='panel-body') else ''
        return f"{title}\n\n{statement}"
