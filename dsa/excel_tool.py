import sys

from PyQt6.QtWidgets import QApplication, QWidget,QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('zxb')
window.resize(500, 500)

btn=QPushButton(text='xxx',parent=window)
window.show()

app.exec()
