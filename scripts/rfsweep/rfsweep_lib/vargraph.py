from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()

data = [0]
raw = serial.Serial('COM9', 115200)


def update():
    global curve, data
    line = raw.readline()
    if ("hand" in line):
        line = line.split(":")
        if len(line) == 8:
            data.append(float(line[4]))
            xdata = np.array(data, dtype='float64')
            curve.setData(xdata)
            app.processEvents()


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
