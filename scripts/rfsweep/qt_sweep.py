import pyqtgraph as pg
import numpy as np
from rfsweep import *
from rfsweep_lib.subfun import *
import argparse

parser = argparse.ArgumentParser(description='rf spectrum analyzer hackrf')
parser.add_argument('--setup', default="pp", type=str,
                    help='realtime or postprocessing')
parser.add_argument("--qt", default=False, type=bool, help="use qt")
parser.add_argument("--freq", default="2400:2500", type=str, help="freq range")

args = parser.parse_args()


class graphf_qt():
    def __init__(self, setbool, min=2400000000, max=2500000000):
        self.max = max
        self.min = min
        self.rf = rfsweep(setbool, min, max, True)
        self.plt = pg.plot()
        self.bufferSize = 1000
        self.data = np.zeros(self.bufferSize)
        self.curve = self.plt.plot()
        self.plt.setRange(xRange=[min, max], yRange=[-100, 0])
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.inter_maj)
        self.timer.start(20)

    def inter_maj(self):
        rand = self.rf.pas()
        lim_data = np.linspace(self.min, self.max, len(rand))

        self.data = rand
        self.curve.setData(lim_data, self.data,)


if __name__ == '__main__':

    min, max = freq_parser(args.freq)

    if args.setup == "pp":
        rf = graphf_qt(False, min, max)
    elif args.setup == "rt":
        rf = graphf_qt(True, min, max)
