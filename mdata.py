from matplotlib.pyplot import axis
import numpy as np
import h5py as hd
import pandas as pd
# import nabPy as Nab

class MData():
    def __init__(self) -> None:
        self.data = None
        self.foldname = None
        self.runno= None
        # self.eventsig = 0xaa55f154
        self.mdata = None
        self.headerinfo = 1
        self.totalevents = 0
        self.dataarea = 0
        self.timebinwidth = 320e-6
        self.bins = 100

    def getdatafromfile(self):
        """
        Load various datas in the current viewer 
        """
        try:
            self.hdFile = Nab.DataRun(self.foldname, self.runno) #We will have to chnage this later so user can input the run number 
            self.fileData = self.hdFile.noiseWaves().headers()
        except:
            pass

    def getDetPixData(self,eventType, det = 'top'):
        self.eventType = eventType
        try:
            self.pixhist = self.hdFile.plotHitLocations(self.eventType, size = 1.3, det = det, rounding='int', onlineanalysis = True, alpha = 0.6, title='1612 File')
        except:
            self.pixhist = np.random.randint(1000, size=127)
        return(self.pixhist)

    def getpixelhistogram(self): 
        self.pixdata = np.array(self.fileData.iloc[:,11])
        # print(len(self.pixdata))
        self.hy,self.hx = np.histogram(self.pixdata)
        # print(self.hx, self.hy)
        # print("getpixelhistogram ran successfully")
        return(self.hy,self.hx)

    def getsingleeventdata(self,eventType='noise',channel='0',eventno=0):
        try:
            self.timeaxis = ((2* np.pi)/300)*np.arange(1000)
            self.pulsedata= 0.5 * np.sin(self.timeaxis) + np.random.random(1000)
            return(self.timeaxis,self.pulsedata)
        except:
            pass
        if eventType == 'noise':
            self.pulsedata = self.hdFile.noiseWaves().waves()[eventno].compute()
        elif eventType == 'singles':
            self.pulsedata = self.hdFile.singleWaves().waves()[eventno].compute()
        else:
            self.pulsedata = self.hdFile.pulsrWaves().waves()[eventno].compute()
        
        self.timeaxis = np.arange(len(self.pulsedata)) * 4e-9
        print(len(self.pulsedata))
        return(self.timeaxis,self.pulsedata)


    #*******************Attempt 2 extracting energies*********************
    ##Generating a list of all energies for each event 
    def getenergyhistogram(self,bins=10,channel=27182):
        try:
            self.energy = np.random.randint(1000, size=5000)
            self.counts ,self.bins = np.histogram(self.energy, self.bins)
            return(self.counts, self.bins)

        except:
            pass
        
        self.bins = bins
        self.trigs = self.hdFile.triggers().triggers()
        if channel == 27182:
            self.energy = self.trigs.query("pixel<128").energy.to_numpy()
        elif channel == 31415:
            self.energy = self.trigs.query("pixel>128").energy.to_numpy()
        else:
            self.energy = self.trigs.query("pixel == @channel").energy.to_numpy()
        
            
        self.counts ,self.bins = np.histogram(self.energy, self.bins)
        
        return(self.counts, self.bins) #maybe instead do self.enerG?? So we can do query in top/bottom detector??

        


