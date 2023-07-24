from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QComboBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

class MainWindow(QWidget):
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

        # Create First Tab
        # self.tab1.layout = QVBoxLayout(self)
        self.mainlayout = QVBoxLayout()
        self.inlayout = QHBoxLayout()
        self.in2layout = QHBoxLayout()
        
        self.foldname = "without data or nabpy installed go to other tabs to check features"
        self.runno = 2447
        
        self.button_foldname = QPushButton('Select Folder')
        self.button_foldname.clicked.connect(self.dialog)
        self.field_foldname = QLineEdit(self.foldname)
        self.field_runno = QLineEdit(str(self.runno))
        
        
        self.data.foldname = self.foldname
        self.data.runno = self.runno
        
        self.button_load = QPushButton('LoadData')
        self.button_load.clicked.connect(self.loaddata)



        self.inlayout.addWidget(self.button_foldname)
        self.inlayout.addWidget(self.field_foldname)
        self.inlayout.addWidget(self.field_runno)
        self.inlayout.addWidget(self.button_load)

        
#********************* Get Second histogram with pix hist (with random data) *******************

        
# #********************* Timer if needed ***********  #
        self.timer = QtCore.QTimer()

#********************* Layouts ***********  #
        self.mainlayout.addLayout(self.inlayout)
        self.mainlayout.addLayout(self.in2layout)

        self.maintab.setLayout(self.mainlayout)

        # Add tabs to Widget
        self.layout.addWidget(self.maintab)
        self.setLayout(self.layout)

#************************************************************************** FUNCTIONS ****************************************************************************************  #

#***************Functions for loading Data *****************************************************#
   
    def dialog(self):
        self.foldname = QFileDialog.getExistingDirectory( None, "Select folder containing data")
        if self.foldname:
            self.fname = self.foldname
            self.field_foldname.setText(self.foldname)
        else:
            self.field_foldname.setText= "folder not found!!"

    def updatefoldname(self):
        self.foldname = self.field_foldname.text()
        self.data.foldname = self.foldname

    def updaterunno(self):
        try:
            self.runno = int(self.field_runno.text())
            # print("what is runno:", self.runno)
            self.data.runno = self.runno
        except:
            self.field_runno.setText("Enter the integer") 
    def loadSummary(self):
        self.xnew = self.data.getDataSummary()
        return(self.xnew)
    
    def updateDataSummary(self):
        self.dataSum = self.data.getDataSummary()
        self.dataSummary.setPlainText(self.dataSum)
        #self.dataSum = self.loadSummary()
        #return(dataSum)


    def loaddata(self):
        """
        Get the data in the data class
        """
        self.updatefoldname()
        self.updaterunno()
        self.data.getdatafromfile()
        self.updateall()
        self.updateDataSummary()
        return(self.data)

        
#**************** Function to update all plots *******************************#
    def updateall(self):
        if self.data is not None:
            print("Mainwindow do not update anything, all plotting is in Topdetector now")

#**************** Function to update Energy histogram *******************************#
    def updateenergyhistogram(self):
        self.edges, self.counts = self.data.getenergyhistogram(bins = 10)
        #self.p2.setData(self.edges, self.counts)
 
#**************** Function to update Single Event *******************************#
    def updatesingleevent(self):
        self.timeax, self.data = self.data.getsingleeventdata(self.eventType,'0',eventno=0)


    def updaterangeplot(self):
        self.getlims()
        self.lims[0] = 0
        self.lims[1] = 20
        x, y = self.data.getrangedata(self.lims[0], self.lims[1], self.chan)
        self.p3.setData(x=x, y=y)
