from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QComboBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
import matplotlib.cm as cmx


# **********************************************
class TopDetector(QWidget):
    # def __init__(self, parent) -> None:
    def __init__(self, data):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        pg.setConfigOption('background', 'w')

        # Initialize DATA
        self.data = data
        # Initialize Tab
        self.maintab = QWidget()

        # self.height
        self.width = 100

        # Creating Layouts
        self.mainlayout = QVBoxLayout()
        self.inlayout = QHBoxLayout()
        self.in2layout = QHBoxLayout()
        self.in3layout = QHBoxLayout()
        self.r1layout = QHBoxLayout()
        self.r2layout = QHBoxLayout()

        self.button_load = QPushButton('LoadData')
        self.button_load.clicked.connect(self.loaddata)

        # Creating dropdown menu to select the channel number
        self.label_channelnum = QLabel("Channel")
        self.label_channelnum.setFixedWidth(60)
        self.sel_channelnum = QComboBox()
        # The channel numbers for top detector are 1-127
        self.sel_channelnum.addItems([str(i+1) for i in np.arange(0,127)]) #The channel numbers for bottom detector are 1-127
        self.sel_channelnum.currentIndexChanged.connect(self.selectchannel)
        self.chan = 0
        self.eventType = 'something'

        self.evtno = 42
        self.energyCut = 'energy', '>', 0
        self.pixelCut = 'pixel', '>', 0

        self.lims = [2, 10]
        self.totevnt = 0
        self.totarea = 0
        self.tbinwidth = 320e-6
        self.evtsig = 0xaa55f154
        self.norm = None

        self.label_Energy = QLabel("Energy Cuts")
        self.value_energyCut = QLineEdit(str(self.energyCut))

        self.label_Pixel = QLabel("Pixel Cuts")
        self.value_pixelCut =QLineEdit(str(self.pixelCut))

        self.button_freerun = QPushButton('FreeRun')
        self.button_freerun.setCheckable(True)
        self.button_freerun.clicked.connect(self.runfreerun)

        self.button_nextevt = QPushButton('Next')
        self.button_nextevt.clicked.connect(self.shownextevent)
        
        self.button_norm = QPushButton('logpixhit')
        self.button_norm.setCheckable(True)
        self.button_norm.clicked.connect(self.selectnormalization)

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
        
        self.inlayout.addWidget(self.button_load)
        self.inlayout.addWidget(self.sel_channelnum)

        self.in3layout.addWidget(self.button_freerun)
        self.in3layout.addWidget(self.button_nextevt)
        self.in3layout.addWidget(self.button_norm)
        self.in3layout.addWidget(self.label_evtno)
        self.in3layout.addWidget(self.value_evtno)

        self.pen1 = pg.mkPen('r', width=2)
        self.pen2 = pg.mkPen(color=(255, 15, 15), width=2)


# ******************** Get PixHits (With random data)   **********************
        self.size = 2
        self.pxplwg = MatplotlibWidget((3.5*self.size, 3.5 * self.size), dpi=100)
        self.pxplwg.vbox.removeWidget(self.pxplwg.toolbar)
        self.pxplwg.toolbar.setVisible(False)
        
        self.pxplfg = self.pxplwg.getFigure()
        
        self.pxplax = self.pxplfg.add_subplot(111)
        
        randompixhist = 100 * np.random.random(127)                                  
        self.customcmap = self.getmycmap(basemap='cividis')           
       
        self.scalarMap = self.plotOneDetector(randompixhist, self.pxplfg, self.pxplax, cmap=self.customcmap)
        self.clbar = self.pxplfg.colorbar(self.scalarMap, ax=self.pxplax)
        

        self.pxplfg.set_tight_layout(tight=True)
 
# ********************* Get Second histogram with pix hist(with random data ***********) *******************

        # self.pw2 = pg.PlotWidget(title="Hit Pixel Data")
        self.pw2 = pg.PlotWidget( title='<span style="color: #000; font-size: 16pt;">Energy Histogram</span>')
        self.p2 = self.pw2.plot(stepMode="center",fillLevel=0)#, fillOutline=True,brush=(100,0,0))
        self.p2.setPen(color=(0, 0, 0), width=2)
        self.pw2.setLabel('left', 'Energy', units='arb')
        self.pw2.setLabel('bottom', 'Bin', units='arb')
        self.pw2.showGrid(x=True, y=True)

# ********************* Third histogram Not used now ************************************

        self.pw3 = pg.PlotWidget(title="Many Events One after other")
        self.p3 = self.pw3.plot()
        self.p3.setPen(color=(0, 0, 0), width=5)
        self.pw3.setLabel('left', 'Value', units='V')
        self.pw3.setLabel('bottom', 'Time', units='s')
        self.pw3.showGrid(x=True, y=True)

        self.noisedata = np.random.random(10)
        self.timeax = np.arange(10)

        self.p3.setData(x=self.timeax, y=self.noisedata)

# ********************* Example of scatter plot if needed ***********  #
        self.pw4 = pg.PlotWidget(title='<span style="color: #000; font-size: 16pt;">Single Event Plot</span>')
        self.pw4.showGrid(x=True, y=True)
        self.pw4.setLabel('left', 'Value', units='arb')
        self.pw4.setLabel('bottom', 'Time', units='arb')

        self.p4 = pg.ScatterPlotItem(size=2, brush=pg.mkBrush(0, 0, 0, 200))
        self.pw4.addItem(self.p4)

        self.noisedata = np.random.random(1000)
        self.timeax = np.arange(1000)
        self.p4.addPoints(x=self.timeax, y=self.noisedata)

# #********************* Timer if needed ***********  #
        self.timer = QtCore.QTimer()

# ********************* Layouts ***********  #
        self.r1layout.addWidget(self.pxplwg)  # PixDec
        self.r1layout.addWidget(self.pw2)
        self.r2layout.addWidget(self.pw4)

        self.mainlayout.addLayout(self.inlayout)
        self.mainlayout.addLayout(self.in3layout)
        self.mainlayout.addLayout(self.r1layout)
        self.mainlayout.addLayout(self.r2layout)

        self.maintab.setLayout(self.mainlayout)

        # Add tabs to Widget
        self.layout.addWidget(self.maintab)
        self.setLayout(self.layout)

# ************************************************************************** FUNCTIONS ****************************************************************************************  #

# ***************Functions for loading Data *****************************************************#

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

    def loaddata(self):
        """
        Get the data in the data class
        """
        self.updateall()

# *************** Functions for Selecting stuff like channen no. event no etc. *****************************************************#
    def selectchannel(self):
        self.chan = int(self.sel_channelnum.currentText())
        self.updateenergyhistogram()
        self.updatesingleevent()


    def selectconditional(self):
        tcond = int(self.sel_conditional.currentText()) - 1
        self.cond = tcond
        self.updateenergyhistogram()
        self.updatesingleevent()

    def selecteventType(self):
        teventType = self.sel_eventType.currentText()

        self.eventType = teventType
        print(self.eventType)
        self.updatesingleevent()
        self.updatepixhits()

    def getevntno(self):
        tempevnt = self.value_evtno.text().split(sep=",")
        self.evtno = int(float(tempevnt[0]))

    def updateevent(self):
        self.getevntno()

    def getEnergyCut(self):
        self.tempEnergy = self.value_energyCut.text().split(sep=",")
        self.energyCut = int(float(self.tempEnergy[0]))

    def updateEnergyCut(self):
        self.getEnergyCut()

    def getPixelCut(self):
        self.tempPixel = self.value_pixelCut.text().split(sep=",")
        self.pixelCut = int(float(self.tempPixel[0]))

    def updatePixelCut(self):
        self.getPixelCut()

# *************** Functions for Updating the plots *****************************************************#

# **************** Function to update all plots *******************************#
    def updateall(self):
        if self.data is not None:
            self.updatepixhits()
            self.updateenergyhistogram()  # SRW commenting out for now to remove errors
            self.updatesingleevent()

# **************** Function to update Energy histogram *******************************
    def updateenergyhistogram(self):
        self.counts, self.edges = self.data.getenergyhistogram(bins = 200,channel=self.chan)
        self.p2.setData(self.edges, self.counts)

# **************** Function to update Single Event *******************************#
    def updatesingleevent(self):
        self.timeax, self.pulsedata = self.data.getsingleeventdata(self.eventType,channel = self.chan,eventno=self.evtno)
        self.p4.setData(self.timeax,self.pulsedata)

# **************** Function to update pixel hits *******************************#
    def updatepixhits(self):
        self.pxplax.cla()
        try:
            self.pixhits= self.data.getDetPixData(self.eventType, det = 'bottom')
        except:
            self.pixhits = np.zeros(127)
            self.pxplax.text(-20,20, 'No Data')
            
        self.scalarMap = self.plotOneDetector(self.pixhits, self.pxplfg, self.pxplax, norm=self.norm,  cmap=self.customcmap, alpha = 0.47)
        self.clbar.update_normal(self.scalarMap)
        self.clbar.update_ticks()
        self.pxplwg.draw()
#


    def updatexy(self):
        if self.data is not None:
            x, y = self.data.getsingle_chan_evnt(self.evtno, self.chan)
            self.p1.setData(x=x, y=y)

    def updaterangeplot(self):
        self.getlims()
        self.lims[0] = 0
        self.lims[1] = 20
        x, y = self.data.getrangedata(self.lims[0], self.lims[1], self.chan)
        self.p3.setData(x=x, y=y)

    def updatedistribution(self):
        hx, hy = self.data.gethistdistribution(self.chan)
        self.p2.setData(hx, hy)


# *************** Other Functions not used now *****************************************************#


    def getlims(self):
        templims = self.value_lims.text().split(sep=",")
        if (len(templims) == 2):
            self.lims = [int(float(i)) for i in templims]
            if (self.lims[1] > self.data.totalevents):
                self.lims[1] = self.data.totalevents - 2
        if (len(self.lims) == 2):
            self.evtno = self.lims[0]
            self.value_evtno.setText(str(self.evtno))
            self.updatexy()

    def updatestackplot(self):
        self.getlims()
        sx, sy = self.data.getstackdata(self.lims[0], self.lims[1], self.chan)
        mx, my = self.data.gettimemean(self.lims[0], self.lims[1], self.chan)
        self.p4.setData(x=sx, y=sy)
        self.p5.setData(x=mx, y=my)

    def runfreerun(self):
        if self.button_freerun.isChecked():
            self.timer.timeout.connect(self.shownextevent)
            self.timer.start(1000)
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
        self.updatesingleevent()

    def showpreviousevent(self):
        self.evtno = self.evtno - 1
        self.value_evtno.setText(str(self.evtno))
        self.updatesingleevent()
        
    def selectnormalization(self):
        if self.button_norm.isChecked():
            self.norm = 'log'
        else:
            self.norm = None
        self.updatepixhits()



# *************** Function to plot detetor hits*****************************************************#
    # this is a simple function that plots values over each pixel
    def plotOneDetector(self, values, fig=None, ax=None, numDet=1, cmap='cividis', size=2, showNum=True, showVal=True, alpha=1, rounding=None, title=None, norm=None, forceMin=None, forceMax=None, labels=None, filename=None, saveDontShow=False):
        ax.set_xlim(-size * 13, size * 13)
        ax.set_ylim(-size * 13, size * 13)
        cm = cmap
        cNorm = None
        minval = np.min(values)
        maxval = np.max(values)
        if forceMin is not None:
            minval = forceMin
        elif norm == 'log':
            if minval <= 0:
                minval = 0.01
        if forceMax is not None:
            maxval = forceMax
        if norm is None:
            cNorm = colors.Normalize(minval, maxval)
        elif norm == 'log':
            cNorm = colors.LogNorm(minval, maxval)
        else:
            print('unrecognized normalization option: needs to be log or not set')
            return (fig, ax)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
        vertOffset = size * np.sqrt(3)
        horOffset = size * 1.5
        colEnd = [7, 15, 24, 34, 45, 57, 70, 82, 93, 103, 112, 120, 127]
        colStart = [1, 8, 16, 25, 35, 46, 58, 71, 83, 94, 104, 113, 121]
        colLen = list(np.array(colEnd) - np.array(colStart) + 1)
        numCol = len(colEnd)
        for pixel in range(1, len(values)+1):
            col = 0
            for j in range(len(colEnd)):
                if pixel >= colStart[j] and pixel <= colEnd[j]:
                    col = j
            # number in the column from the top of the column
            numInCol = pixel - colStart[col]
            horPosition = (col - numCol/2)*horOffset
            topOfCol = colLen[col]/2*vertOffset - vertOffset/2
            verPosition = topOfCol - vertOffset*numInCol
            hex = patches.RegularPolygon((horPosition, verPosition), numVertices=6, radius=size, facecolor=scalarMap.to_rgba(
                values[pixel-1]), orientation=np.pi/2, alpha=alpha, edgecolor='black')
            ax.add_patch(hex)
            txt = ''
            if showNum == True:
                txt += str(pixel)
            if labels is not None:
                if txt != '':
                    txt += '\n'
                txt += str(labels[pixel-1])
            if showVal:
                if txt != '':
                    txt += '\n'
                if rounding is not None:
                    if rounding == 'int':
                        txt += str(int(values[pixel-1]))
                    else:
                        txt += str(round(values[pixel-1], rounding))
            if txt != '':
                ax.text(horPosition-size/2, verPosition,
                        txt, ma='center', va='center')
        return scalarMap

    def getmycmap(self, basemap='viridis'):
        ocmap = plt.get_cmap(basemap)
        ocmap = ocmap(np.linspace(0, 1, 256))
        ocmap[:1, :] = ([0.95, 0.95, 0.95, 1])
        ncmap = colors.ListedColormap(ocmap)
        return (ncmap)