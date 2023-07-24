from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QComboBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
from mdata import MData


class Flipper(QWidget):
    # def __init__(self, parent) -> None:
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        pg.setConfigOption('background', 'w')

        # Initialize DATAS
        self.ped = MData()
        self.nhe = MData()
        self.yhe = MData()

        # Initialize Tab
        self.maintab = QWidget()

        # self.height
        self.width = 100
        self.lims = [2, 1000]
        self.pedvcut = 0
        self.nhevcut = 0
        self.yhevcut = 0
        self.fliprat = None
        self.flipratmean = 0.00
        # self.totevnt = 0
        # self.totarea = 0
        # self.tbinwidth = 320e-6
        self.evtsig = 0xaa55f154

        # Create First Tab
        # self.tab1.layout = QVBoxLayout(self)
        self.mainlayout = QVBoxLayout()
        self.pedlayout = QHBoxLayout()
        self.nhelayout = QHBoxLayout()
        self.yhelayout = QHBoxLayout()
        self.r0layout = QHBoxLayout()
        self.r1layout = QHBoxLayout()
        self.r2layout = QHBoxLayout()

        self.button_pedfname = QPushButton('Pedastal File/s')
        self.button_nhefname = QPushButton('With He  File/s')
        self.button_yhefname = QPushButton('Wout He File/s')

        self.pedfname = "/Users/seeker/TNwork/picarddata/2022/01Jan/070122/run-16040data-21"
        self.nhefname = "/Users/seeker/TNwork/picarddata/2022/01Jan/070122/run-16043data-21"
        self.yhefname = "/Users/seeker/TNwork/picarddata/2022/01Jan/070122/run-16053data-21"

        self.field_pedfname = QLineEdit(self.pedfname)
        self.field_yhefname = QLineEdit(self.nhefname)
        self.field_nhefname = QLineEdit(self.yhefname)

        self.button_pedfname.clicked.connect(
            lambda: self.dialog(self.pedfname, self.field_pedfname))
        self.button_nhefname.clicked.connect(
            lambda: self.dialog(self.nhefname, self.field_nhefname))
        self.button_yhefname.clicked.connect(
            lambda: self.dialog(self.yhefname, self.field_yhefname))

        self.field_pedfname.textChanged.connect(
            lambda: self.updatefname("ped"))
        self.field_nhefname.textChanged.connect(
            lambda: self.updatefname("nhe"))
        self.field_yhefname.textChanged.connect(
            lambda: self.updatefname("yhe"))

        self.label_pedchanno = QLabel("Ped Channel")
        self.label_nhechanno = QLabel("No He Channel")
        self.label_yhechanno = QLabel("He Channel")

        self.label_pedchanno.setFixedWidth(60)
        self.label_nhechanno.setFixedWidth(60)
        self.label_yhechanno.setFixedWidth(60)

        self.ped.fname = self.pedfname
        self.nhe.fname = self.nhefname
        self.yhe.fname = self.yhefname

        self.button_pedload = QPushButton('LoadData')
        self.button_nheload = QPushButton('LoadData')
        self.button_yheload = QPushButton('LoadData')

        self.button_pedload.clicked.connect(lambda: self.loaddata(
            self.field_pedfname, self.pedfname, self.ped, self.p1, self.p1m, self.pedchan))
        self.button_nheload.clicked.connect(lambda: self.loaddata(
            self.field_nhefname, self.nhefname, self.nhe, self.p2, self.p2m, self.nhechan))
        self.button_yheload.clicked.connect(lambda: self.loaddata(
            self.field_yhefname, self.yhefname, self.yhe, self.p3, self.p3m, self.yhechan))

        self.sel_pedchanno = QComboBox()
        self.sel_nhechanno = QComboBox()
        self.sel_yhechanno = QComboBox()

        self.sel_pedchanno.addItems([str(i + 1) for i in np.arange(24)])
        self.sel_nhechanno.addItems([str(i + 1) for i in np.arange(24)])
        self.sel_yhechanno.addItems([str(i + 1) for i in np.arange(24)])

        self.sel_pedchanno.currentIndexChanged.connect(self.selectchannel)
        self.sel_nhechanno.currentIndexChanged.connect(self.selectchannel)
        self.sel_yhechanno.currentIndexChanged.connect(self.selectchannel)

        self.label_lims = QLabel("Range")
        self.label_lims.setFixedWidth(60)
        self.label_pedvcut = QLabel("pedVCut")
        self.label_pedvcut.setFixedWidth(60)
        self.label_nhevcut = QLabel("nheVCut")
        self.label_nhevcut.setFixedWidth(60)
        self.label_yhevcut = QLabel("vheVCut")
        self.label_yhevcut.setFixedWidth(60)

        self.value_lims = QLineEdit(str(self.lims)[1:-1])
        self.value_lims.setFixedWidth(60)
        self.value_lims.textChanged.connect(self.updateallstackplot)
        self.value_pedvcut = QLineEdit(str(self.pedvcut))
        self.value_pedvcut.setFixedWidth(60)
        self.value_pedvcut.textChanged.connect(
            lambda: self.updatevcuts(self.value_pedvcut, self.ped))
        self.value_nhevcut = QLineEdit(str(self.nhevcut))
        self.value_nhevcut.setFixedWidth(60)
        self.value_nhevcut.textChanged.connect(
            lambda: self.updatevcuts(self.value_nhevcut, self.nhe))
        self.value_yhevcut = QLineEdit(str(self.yhevcut))
        self.value_yhevcut.setFixedWidth(60)
        self.value_yhevcut.textChanged.connect(
            lambda: self.updatevcuts(self.value_yhevcut, self.yhe))

        self.pedchan = 1
        self.nhechan = 1
        self.yhechan = 1

        self.fliprat = 0.0

        self.label_fliprat = QLabel("FlippingRatio")
        # self.label_fliprat.setFixedWidth(60)
        self.value_fliprat = QLineEdit(str(self.fliprat))
        # self.value_fliprat.setFixedWidth(60)
        self.button_fliprat= QPushButton('GetFlipRat')
        self.button_fliprat.clicked.connect(self.flippingratio)
        # self.label_space= QLabel(" ")
 

        # self.button_freerun = QPushButton('FreeRun')
        # self.button_freerun.setCheckable(True)
        # self.button_freerun.clicked.connect(self.runfreerun)

        # self.button_nextevt = QPushButton('Next')
        # self.button_nextevt.clicked.connect(self.shownextevent)

        # self.label_evtno = QLabel("Event")
        # # self.label_evtno.setFixedWidth(60)
        # self.value_evtno = QLineEdit(str(self.evtno))

        # self.label_totevt = QLabel("Total Event")
        # # self.label_totevt.setFixedWidth(60)
        # self.value_totevt = QLineEdit(str(self.totevnt))

        # self.label_totarea = QLabel("Area")
        # # self.label_totarea.setFixedWidth(60) # test
        # self.value_totarea = QLineEdit(str(self.totarea))

        # self.value_evtno.textChanged.connect(self.updateevent)
        # self.label_lims = QLabel("Range")
        # self.value_lims = QLineEdit(str(self.lims)[1:-1])
        # self.label_lims.setFixedWidth(60)
        # self.value_lims.textChanged.connect(self.updatestackplot)
        # self.field_fname.setMaximumWidth(self.width)
        # self.space = QSpacerItem(10,5)

        self.pedlayout.addWidget(self.button_pedfname)
        self.pedlayout.addWidget(self.field_pedfname)
        self.pedlayout.addWidget(self.button_pedload)
        self.pedlayout.addWidget(self.label_pedchanno)
        self.pedlayout.addWidget(self.sel_pedchanno)

        self.nhelayout.addWidget(self.button_nhefname)
        self.nhelayout.addWidget(self.field_nhefname)
        self.nhelayout.addWidget(self.button_nheload)
        self.nhelayout.addWidget(self.label_nhechanno)
        self.nhelayout.addWidget(self.sel_nhechanno)

        self.yhelayout.addWidget(self.button_yhefname)
        self.yhelayout.addWidget(self.field_yhefname)
        self.yhelayout.addWidget(self.button_yheload)
        self.yhelayout.addWidget(self.label_yhechanno)
        self.yhelayout.addWidget(self.sel_yhechanno)

        self.r0layout.addWidget(self.label_lims)
        self.r0layout.addWidget(self.value_lims)
        self.r0layout.addWidget(self.label_pedvcut)
        self.r0layout.addWidget(self.value_pedvcut)
        self.r0layout.addWidget(self.label_nhevcut)
        self.r0layout.addWidget(self.value_nhevcut)
        self.r0layout.addWidget(self.label_yhevcut)
        self.r0layout.addWidget(self.value_yhevcut)
        self.r0layout.addWidget(self.label_fliprat)
        self.r0layout.addWidget(self.value_fliprat)
        self.r0layout.addWidget(self.button_fliprat)
        # self.r0layout.addWidget(self.label_space)

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
#  Pedestal Run
        self.pw1 = pg.PlotWidget(title="Pedestal Run")
        self.p1 = pg.ScatterPlotItem(size=2, brush=pg.mkBrush(0, 0, 0, 200))
        self.p1.addPoints(x=self.x, y=self.y)

        self.p1m = self.pw1.plot()
        self.p1m.setPen(color=(0, 0, 0), width=2)
        self.p1m.setData(x=self.x, y=self.y)

        self.pw1.addItem(self.p1)
        self.pw1.setLabel('left', 'Value', units='V')
        self.pw1.setLabel('bottom', 'Time', units='s')
        self.pw1.showGrid(x=True, y=True)

#  No Helium Run
        self.pw2 = pg.PlotWidget(title="Run Without Helium Cell")
        self.p2 = pg.ScatterPlotItem(size=2, brush=pg.mkBrush(0, 0, 0, 200))
        self.p2.addPoints(x=self.x, y=self.y)

        self.p2m = self.pw2.plot()
        self.p2m.setPen(color=(0, 0, 0), width=2)
        self.p2m.setData(x=self.x, y=self.y)

        self.pw2.addItem(self.p2)
        self.pw2.setLabel('left', 'Value', units='V')
        self.pw2.setLabel('bottom', 'Time', units='s')
        self.pw2.showGrid(x=True, y=True)

#  Helium Run
        self.pw3 = pg.PlotWidget(title="Run With Helium Cell")
        self.p3 = pg.ScatterPlotItem(size=2, brush=pg.mkBrush(0, 0, 0, 200))
        self.p3.addPoints(x=self.x, y=self.y)

        self.p3m = self.pw3.plot()
        self.p3m.setPen(color=(0, 0, 0), width=2)
        self.p3m.setData(x=self.x, y=self.y)

        self.pw3.addItem(self.p3)
        self.pw3.setLabel('left', 'Value', units='V')
        self.pw3.setLabel('bottom', 'Time', units='s')
        self.pw3.showGrid(x=True, y=True)

#   Blank
        self.pw4 = pg.PlotWidget(title="Left Blank")
        self.p4 = pg.ScatterPlotItem(size=2, brush=pg.mkBrush(0, 0, 0, 200))

        # self.p4 = self.pw4.plot(stepMode="center")
        #  fillLevel=0, fillOutline=True,brush=(100,0,0))
        # self.p4.setPen(color=(0, 0, 0), width=2)
        self.pw4.addItem(self.p4)
        self.pw4.setLabel('left', 'FlipRat', units='arb')
        self.pw4.setLabel('bottom', 'Time', units='s')
        self.p4.setData(self.x, self.y)
        self.pw4.showGrid(x=True, y=True)

        self.timer = QtCore.QTimer()

        self.r1layout.addWidget(self.pw1)
        self.r1layout.addWidget(self.pw2)
        self.r2layout.addWidget(self.pw3)
        self.r2layout.addWidget(self.pw4)

        self.mainlayout.addLayout(self.pedlayout)
        self.mainlayout.addLayout(self.nhelayout)
        self.mainlayout.addLayout(self.yhelayout)
        self.mainlayout.addLayout(self.r0layout)
        self.mainlayout.addLayout(self.r1layout)
        self.mainlayout.addLayout(self.r2layout)
        # self.alayout.addWidget(self.pw1)
        # self.alayout.addWidget(self.pw2)

        self.maintab.setLayout(self.mainlayout)
        # self.tab1.setLayout(self.alayout)

        # Add tabs to Widget
        self.layout.addWidget(self.maintab)
        self.setLayout(self.layout)

    def dialog(self, fname, fnamefield):
        # file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        tempfile, check = QFileDialog.getOpenFileName(
            None, "SelectFile", "", "")
        if check:
            fname = tempfile
            fnamefield.setText(fname)
        else:
            fname = "file not found!!"
        del fname

    def selectchannel(self):
        pass
        # tchan = int(self.sel_channo.currentText()) - 1
        # # print(tchan, type(tchan))
        # self.chan = tchan
        # self.value_totarea.setText(str(self.data.getarea(self.chan)))
        # self.updateall()

    def getevntno(self):
        tempevnt = self.value_evtno.text().split(sep=",")
        self.evtno = int(float(tempevnt[0]))

    def updateevent(self):
        self.getevntno()
        self.updatexy()

    def loaddata(self, fnamefield, fname, data, pl, plm, chan):
        """
        Get the data in the form of array of 48x40 (2d array)(48 channel column, and 40 rows which are samples)
        """
        # GET OFFSET
        fnamefield.setStyleSheet(
            "color: black;  background-color: white")
        print(fname)
        data.fname = fname
        tfname = fname
        if(data.getdatafromfile() == 0):
            fnamefield.setText(
                "WARNING: ThIs FiLe Do NoT CoNtAiN PrOpEr HeAdEr")
            fnamefield.setStyleSheet(
                "color: black;  background-color: red")
            fname = tfname
        del tfname
        # self.value_totevt.setText(str((self.data.totalevents)))
        # self.value_totarea.setText(str(self.data.getarea(self.chan)))

        self.updatestackplot(data, pl, plm, chan)
        del data
        del fname
        # return(data)

    def updateall(self):
        if self.data is not None:
            self.updatestackplot()

    def updatexy(self):
        if self.data is not None:
            x, y = self.data.getsingle_chan_evnt(self.evtno, self.chan)
            self.p1.setData(x=x, y=y)

    def updaterangeplot(self):
        self.getlims()
        self.lims[0] = 0
        self.lims[1] = 2000
        x, y = self.data.getrangedata(self.lims[0], self.lims[1], self.chan)
        self.p3.setData(x=x, y=y)

    def updatedistribution(self):
        hx, hy = self.data.gethistdistribution(self.chan)
        self.p2.setData(hx, hy)

    def updatefname(self, runtype):
        if runtype == "ped":
            self.pedfname = self.field_pedfname.text()
        if runtype == "nhe":
            self.nhefname = self.field_nhefname.text()
        if runtype == "yhe":
            self.yhefname = self.field_yhefname.text()

    def getlims(self, data):
        templims = self.value_lims.text().split(sep=",")
        if(len(templims) == 2):
            self.lims = [int(float(i)) for i in templims]
            if(self.lims[1] > data.totalevents):
                self.lims[1] = data.totalevents - 2

    def updatestackplot(self, data, pl, plm, chan):
        self.getlims(data)
        self.lims = [10, 100]
        sx, sy = data.getstackdata(self.lims[0], self.lims[1], chan)
        mx, my = data.gettimemean(self.lims[0], self.lims[1], chan)
        pl.setData(x=sx, y=sy)
        plm.setData(x=mx, y=my)

    def updateallstackplot(self):
        self.updatestackplot(self.ped, self.p1, self.p1m, self.pedchan)
        self.updatestackplot(self.nhe, self.p2, self.p2m, self.nhechan)
        self.updatestackplot(self.yhe, self.p3, self.p3m, self.yhechan)

    def getarea(self):
        if self.data is not None:
            # talldata = self.data[0:len(self.data)-1,self.chan].flatten()
            talldata = self.data[:, self.chan].flatten()

            # print(talldata.sum())
            self.value_totarea.setText(str(talldata.sum()))

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

    def updatevcuts(self, vcutfield, data):
        tvcut = vcutfield.text().split(sep=",")
        tvcut = int(float(tvcut[0]))
        data.applyvcut(tvcut)
        self.updateallstackplot()

    def flippingratio(self):
        self.tx,pedtminy = self.ped.gettimemean(chan=self.pedchan)
        self.tx,nhetminy = self.nhe.gettimemean(chan=self.nhechan)
        self.tx,yhetminy = self.yhe.gettimemean(chan=self.yhechan)

        self.fliprat = (yhetminy-pedtminy) / (nhetminy-pedtminy)
        self.p4.setData(self.tx, self.fliprat)
        self.flipratmean = self.fliprat.mean()
        self.value_fliprat.setText(str(self.flipratmean))
