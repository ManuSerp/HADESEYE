import sys

import threading

import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import rfsweep


class App(QtGui.QMainWindow):
    def __init__(self, buffer_size=0, data_buffer=[], graph_title="", parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)

        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        self.view.setRange(QtCore.QRectF(2400, -100, 2500, 0))

        self.numDstreams = 1
        self.bufferLength = buffer_size
        self.graphTitle = graph_title

        self.otherplot = [[self.canvas.addPlot(row=i, col=0, title=self.graphTitle)]  # , repeat line for more
                          for i in range(0, self.numDstreams)]
        # , self.otherplot[i][1].plot(pen='g'), self.otherplot[i][2].plot(pen='b')
        self.h2 = [[self.otherplot[i][0].plot(
            pen='r')] for i in range(0, self.numDstreams)]
        # ,np.zeros((1,self.bufferLength)),np.zeros((1,self.bufferLength))
        self.ydata = [[np.zeros((1, self.bufferLength))]
                      for i in range(0, self.numDstreams)]  # axis

        for i in range(0, self.numDstreams):
            self.otherplot[i][0].setYRange(min=-100, max=100)

        self.update_plot(data_buffer)

    def update_plot(self, data):
        self.dataBuffer = data
        for i in range(0, self.numDstreams):
            self.ydata[i][0] = np.array(self.dataBuffer)
            self.h2[i][0].setData(self.ydata[i][0])


def CreateGraph(graph_title):
    thisapp1 = App(graph_title=graph_title)
    thisapp1.show()
    return thisapp1


class Helper(QtCore.QObject):
    bufferChanged = QtCore.pyqtSignal(object)


def generate_buffer(helper):
    while 1:
        test_buffer = [1 for i in range(0, 100)]
        helper.bufferChanged.emit(test_buffer)
        QtCore.QThread.msleep(1)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    graph = CreateGraph("freq power")
    helper = Helper()
    threading.Thread(target=generate_buffer, args=(
        helper, ), daemon=True).start()
    helper.bufferChanged.connect(graph.update_plot)

    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(app.exec_())
