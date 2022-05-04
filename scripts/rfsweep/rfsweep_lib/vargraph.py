from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
import pyqtgraph as pg
import time
import sys


class graphf_qt():
    def __init__(self, min=2400000000, max=2500000000):
        self.max = max
        self.min = min
        self.app = QtWidgets.QApplication([])
        self.p = pg.plot()
        self.p.setWindowTitle('live plot from the hackrf')
        self.curve = self.p.plot()
        self.data = [0 for i in range(100)]
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.inter_maj)
        self.timer.start(0)
        self.launch()

    def inter_maj(self):
        xdata = np.array(self.data)
        lim_data = np.linspace(self.min, self.max, len(xdata))
        self.curve.setData(lim_data, xdata)

        self.app.processEvents()

    def update(self, y_buffer):
        self.data = y_buffer

    def launch(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec_()


if __name__ == '__main__':
    g = graphf_qt()

    g.update([1, 2, 3])
    g.update([-60, 50, -40])
