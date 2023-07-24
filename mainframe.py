from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
import pyqtgraph as pg
from mainwindow import MainWindow
from monitorwindow import Monitor
from flippingratio import Flipper
from mdata import MData
from topdetector import TopDetector 
from bottomdetector import BottomDetector 



class MainFrame(QWidget):
    def __init__(self, parent) -> None:
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        pg.setConfigOption('background', 'w')

        # Define Data
        self.data = MData()

        # Define Tabs
        self.tabs = QTabWidget()
        self.tab1 = MainWindow(self.data)
        self.tab2 = TopDetector(self.data) 
        self.tab3 = BottomDetector(self.data) 
        # self.tab3 = Monitor(self.data)
        self.tab4 = Flipper()
        self.tab5 = Monitor(self.data)

        # Add Tabs
        self.tabs.addTab(self.tab1, "Main Window")
        self.tabs.addTab(self.tab2, "Top Detector")
        self.tabs.addTab(self.tab3, "Bottom Detector")
        self.tabs.addTab(self.tab4, "Slow Control")
        self.tabs.addTab(self.tab5, "FPGA")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

