import sys
import matplotlib.pyplot as plt
# plt.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.size = 3
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig, ax = plt.subplots(1, figsize=(size * 7 + size, size * 7), constrained_layout = True)


def plotOneDetector(values, numDet = 1, cmap = 'cividis', size = 3, showNum = True, showVal = True, alpha=1, rounding = None, title = None, norm = None, forceMin = None, forceMax = None, labels=None, filename = None, saveDontShow = False): #this is a simple function that plots values over each pixel
	ax.set_xlim(-size * 13, size * 13)
	ax.set_ylim(-size * 13, size * 13)
	cm = plt.get_cmap(cmap)
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
		return
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
		numInCol = pixel - colStart[col] #number in the column from the top of the column
		horPosition = (col - numCol/2)*horOffset
		topOfCol = colLen[col]/2*vertOffset - vertOffset/2
		verPosition = topOfCol - vertOffset*numInCol
		hex = patches.RegularPolygon((horPosition, verPosition), numVertices=6, radius=size, facecolor=scalarMap.to_rgba(values[pixel-1]), orientation=np.pi/2, alpha = alpha, edgecolor='black')
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
		if txt!='':
			ax.text(horPosition-size/2, verPosition, txt, ma='center', va='center')
	#axColor = plt.axes([size*6, size*-6, size, size*])
	#plt.colorbar(scalarMap, cax = axColor, orientation="vertical")
	fig.colorbar(scalarMap, ax=ax)
	plt.axis('off')
	if title is not None:
		plt.title(title)
	if filename is not None:
		plt.savefig(filename)
		if saveDontShow == True:
			plt.clf()
			return
	else:
		if saveDontShow == True:
			print('need to pass a name if you want to save the file')
			plt.clf()
			return
		plt.show()
		return
	return