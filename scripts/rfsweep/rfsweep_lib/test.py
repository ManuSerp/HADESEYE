import pyqtgraph as pg
import numpy as np


class graphf_qt():
    def __init__(self, min=2400000000, max=2500000000):
        self.max = max
        self.min = min
        self.plt = pg.plot()
        self.bufferSize = 1000
        self.data = np.zeros(self.bufferSize)
        self.curve = self.plt.plot()
        self.plt.setRange(xRange=[0, self.bufferSize], yRange=[-50, 50])
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.inter_maj)
        self.timer.start(20)

    def inter_maj(self):
        # n = self.bufferSize
        # rand = np.random.normal(size=n)
        # self.data = rand
        self.curve.setData(self.data)


if __name__ == '__main__':
    g = graphf_qt()

    for i in range(100000000):
        print(i)
        n = 1000
        rand = np.random.normal(size=n)
        g.data = rand
