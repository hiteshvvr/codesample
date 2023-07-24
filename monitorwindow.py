from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QComboBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np


class Monitor(QWidget):
    # def __init__(self, parent) -> None:
    def __init__(self,data):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        pg.setConfigOption('background', 'w')

        # Initialize DATA
        self.data = data
        # Initialize Tab
        self.maintab = QWidget()

        # self.height
        self.width = 100

        # Create First Tab
        # self.tab1.layout = QVBoxLayout(self)
        self.mainlayout = QVBoxLayout()
        self.inlayout = QHBoxLayout()
        self.in2layout = QHBoxLayout()
        self.r1layout = QHBoxLayout()
        self.r2layout = QHBoxLayout()

        self.label_channo = QLabel("Channel")
        self.label_channo.setFixedWidth(60)
        self.sel_channo = QComboBox()
        self.sel_channo.addItems([str(i+1) for i in np.arange(24)])
        self.sel_channo.currentIndexChanged.connect(self.selectchannel)
        self.chan = 0

        self.evtno = 42
        self.lims = [2, 10]
        self.totevnt = 00
        self.totarea = 00
        self.tbinwidth = 320e-6
        self.evtsig = 0xaa55f154

        self.button_freerun = QPushButton('FreeRun')
        self.button_freerun.setCheckable(True)
        self.button_freerun.clicked.connect(self.runfreerun)

        self.button_nextevt = QPushButton('Next')
        self.button_nextevt.clicked.connect(self.shownextevent)

        self.label_evtno = QLabel("Event")
        # self.label_evtno.setFixedWidth(60)
        self.value_evtno = QLineEdit(str(self.evtno))

        self.label_totevt = QLabel("Total Event")
        # self.label_totevt.setFixedWidth(60)
        self.value_totevt = QLineEdit(str(self.totevnt))

        self.label_totarea = QLabel("Area")
        # self.label_totarea.setFixedWidth(60)
        self.value_totarea = QLineEdit(str(self.totarea))

        self.value_evtno.textChanged.connect(self.updateevent)
        self.label_lims = QLabel("Range")
        self.value_lims = QLineEdit(str(self.lims)[1:-1])
        self.label_lims.setFixedWidth(60)
        self.value_lims.textChanged.connect(self.updatestackplot)
        # self.field_fname.setMaximumWidth(self.width)
        # self.space = QSpacerItem(10,5)

        # self.inlayout.addWidget(self.button_fname)
        # self.inlayout.addWidget(self.field_fname)
        # self.inlayout.addWidget(self.button_load)

        self.in2layout.addWidget(self.label_channo)
        self.in2layout.addWidget(self.sel_channo)
        self.in2layout.addWidget(self.button_freerun)
        self.in2layout.addWidget(self.button_nextevt)
        self.in2layout.addWidget(self.label_evtno)
        self.in2layout.addWidget(self.value_evtno)
        self.in2layout.addWidget(self.label_lims)
        self.in2layout.addWidget(self.value_lims)

        self.in2layout.addWidget(self.label_totevt)
        self.in2layout.addWidget(self.value_totevt)
        self.in2layout.addWidget(self.label_totarea)
        self.in2layout.addWidget(self.value_totarea)

        # self.gwin = pg.GraphicsWindow()
        # self.rplt = self.gwin.addPlot()

        self.pen1 = pg.mkPen('r', width=2)
        self.pen2 = pg.mkPen(color=(255, 15, 15), width=2)
        # self.pen3 = pg.mkPen(color=(000, 155, 115), style=QtCore.Qt.DotLine)
        # self.curve = self.rplt.plot(pen=self.pen3)
        # self.curve2 = self.rplt.plot(pen=self.pen2)
        # self.rplt.showGrid(x=True, y=True)
        # self.data = np.arange(100)
        # self.avg_data = []
        # self.count = 0
        # self.curve.setData(self.data)

#       INITIAL RANDOM DATA
        self.x = np.arange(100)
        self.y = np.random.random(100)
        self.bins = 40
        self.hy, self.hx = np.histogram(self.y, bins=self.bins)

#       PLOTS

        self.pw1 = pg.PlotWidget(title="Single Event")
        self.pen1 = pg.mkPen(
            color=(000, 0, 0), style=QtCore.Qt.DotLine, width=2)
        self.p1 = self.pw1.plot(pen=self.pen1)
        self.pw1.title = "adf"
        # self.p1.setPen(color = (0,0,0), width = 2)
        self.pw1.setLabel('left', 'Value', units='V')
        self.pw1.setLabel('bottom', 'Time', units='s')
        self.p1.setData(x=self.x, y=self.y)
        self.pw1.showGrid(x=True, y=True)

        self.pw2 = pg.PlotWidget(title="Histogram of all Events")

        self.p2 = self.pw2.plot(stepMode="center")
        #  fillLevel=0, fillOutline=True,brush=(100,0,0))
        self.p2.setPen(color=(0, 0, 0), width=2)
        self.pw2.setLabel('left', 'Counts', units='arb')
        self.pw2.setLabel('bottom', 'Volts', units='V')
        self.p2.setData(self.hx, self.hy)
        self.pw2.showGrid(x=True, y=True)

        self.pw3 = pg.PlotWidget(title="Many Events One after other")
        self.p3 = self.pw3.plot()
        self.p3.setPen(color=(0, 0, 0), width=5)
        self.pw3.setLabel('left', 'Value', units='V')
        self.pw3.setLabel('bottom', 'Time', units='s')
        self.p3.setData(x=self.x, y=self.y)
        self.pw3.showGrid(x=True, y=True)

        self.pw4 = pg.PlotWidget(title="Stacked Events")
        self.p4 = pg.ScatterPlotItem(size=2, brush=pg.mkBrush(0, 0, 0, 200))
        self.p4.addPoints(x=self.x, y=self.y)

        self.p5 = self.pw4.plot()
        #  fillLevel=0, fillOutline=True,brush=(100,0,0))
        self.p5.setPen(color=(0, 0, 0), width=2)
        self.p5.setData(self.x, self.y)

        self.pw4.addItem(self.p4)
        self.pw4.setLabel('left', 'Value', units='V')
        self.pw4.setLabel('bottom', 'Time', units='s')
        # self.p4.setData(x=self.x, y = self.y)
        # self.pw4.showGrid(x=True, y=True)

        self.timer = QtCore.QTimer()

        self.r1layout.addWidget(self.pw1)
        self.r1layout.addWidget(self.pw2)
        self.r2layout.addWidget(self.pw3)
        self.r2layout.addWidget(self.pw4)

        # self.alayout.addWidget(self.setallVolt)
        # self.alayout.addWidget(self.gwin)
        # self.alayout.addLayout(self.inlayout)
        # self.mainlayout.addLayout(self.inlayout)
        self.mainlayout.addLayout(self.in2layout)
        self.mainlayout.addLayout(self.r1layout)
        self.mainlayout.addLayout(self.r2layout)
        # self.alayout.addWidget(self.pw1)
        # self.alayout.addWidget(self.pw2)

        self.maintab.setLayout(self.mainlayout)
        # self.tab1.setLayout(self.alayout)

        # Add tabs to Widget
        self.layout.addWidget(self.maintab)
        self.setLayout(self.layout)

    def dialog(self):
        # file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        tempfile, self.check = QFileDialog.getOpenFileName(
            None, "SelectFile", "", "")
        if self.check:
            self.fname = tempfile
            self.field_fname.setText(self.fname)
            # print(type(tempfile))
        else:
            self.file = "file not found!!"

    def selectchannel(self):
        tchan = int(self.sel_channo.currentText()) - 1
        # print(tchan, type(tchan))
        self.chan = tchan
        self.value_totarea.setText(str(self.data.getarea(self.chan)))
        self.updateall()

    def getevntno(self):
        tempevnt = self.value_evtno.text().split(sep=",")
        self.evtno = int(float(tempevnt[0]))

    def updateevent(self):
        self.getevntno()
        self.updatexy()

    def loaddata(self):
        """
        Get the data in the form of array of 48x40 (2d array)(48 channel column, and 40 rows which are samples)
        """
        # GET OFFSET
        self.field_fname.setStyleSheet( "color: black;  background-color: white")
        self.data.fname = self.fname
        tfname = self.fname
        if(self.data.getdatafromfile() == 0):
            self.field_fname.setText("WARNING: ThIs FiLe Do NoT CoNtAiN PrOpEr HeAdEr")
            self.field_fname.setStyleSheet("color: black;  background-color: red")
            self.fname = tfname
        del tfname
        self.value_totevt.setText(str((self.data.totalevents)))
        self.value_totarea.setText(str(self.data.getarea(self.chan)))


        self.updateall()
        return(self.data)

    def updateall(self):
        if self.data is not None:
            self.updatexy()
            self.updaterangeplot()
            self.updatedistribution()
            self.updatestackplot()

    def updatexy(self):
        if self.data is not None:
            x,y = self.data.getsingle_chan_evnt(self.evtno, self.chan)
            self.p1.setData(x=x,y=y)

    def updaterangeplot(self):
        self.getlims()
        self.lims[0] = 0
        self.lims[1] = 20
        x,y = self.data.getrangedata(self.lims[0], self.lims[1],self.chan)
        self.p3.setData(x=x, y=y)

    def updatedistribution(self):
        hx, hy = self.data.gethistdistribution(self.chan)
        self.p2.setData(hx, hy)

    def updatefname(self):
        self.fname = self.field_fname.text()

    def getlims(self):
        templims = self.value_lims.text().split(sep=",")
        if(len(templims) == 2):
            self.lims = [int(float(i)) for i in templims]
            if(self.lims[1] > self.data.totalevents):
                self.lims[1] = self.data.totalevents - 2
        if(len(self.lims) == 2):
            self.evtno = self.lims[0]
            self.value_evtno.setText(str(self.evtno))
            self.updatexy()

    def updatestackplot(self):
        self.getlims()
        sx,sy = self.data.getstackdata(self.lims[0],self.lims[1],self.chan)
        mx,my = self.data.gettimemean(self.lims[0],self.lims[1],self.chan)
        self.p4.setData(x=sx, y=sy)
        self.p5.setData(x=mx , y=my)

    def runfreerun(self):
        if self.button_freerun.isChecked():
            self.timer.timeout.connect(self.randxy)
            self.timer.start(2000)
        else:
            self.timer.stop()

    def randxy(self):
        if self.data is not None:
            datalen = self.data.totalevents
            self.evtno = np.random.randint(datalen)
            self.value_evtno.setText(str(self.evtno))
            self.updatexy()

    def shownextevent(self):
        self.evtno = self.evtno + 1
        self.value_evtno.setText(str(self.evtno))
        self.updatexy()
