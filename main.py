import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory
from mainframe import MainFrame


class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Nab Online Monitor and Analysis"
        self.setWindowTitle(self.title)
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.tab_widget = MainFrame(self)
        self.setCentralWidget(self.tab_widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
