import pyqtgraph as pg
import numpy as np
from rfsweep import *
from rfsweep_lib.subfun import *
import argparse
from rfsweep_lib.siglocate import *

parser = argparse.ArgumentParser(description='rf spectrum analyzer hackrf')
parser.add_argument('--setup', default="pp", type=str,
                    help='realtime or postprocessing')
parser.add_argument("--qt", default=False, type=bool, help="use qt")
parser.add_argument("--freq", default="2400:2500", type=str, help="freq range")
parser.add_argument("--mode", default=1, type=int,
                    help="mode 1 to erase noise")

args = parser.parse_args()


def cal_dist(g, A=-35.5):
    return pow(10, (A-g)/20)


class graphf_qt():
    def __init__(self, setbool, min=2400000000, max=2500000000, mode=0):
        self.max = max
        self.min = min
        self.rf = rfsweep(setbool, min, max, True, mode)
        self.app = pg.mkQApp("app")
#mw = QtWidgets.QMainWindow()
# mw.resize(800,800)

        self.win = pg.GraphicsLayoutWidget(
            show=True, title="HADES EYE Window")
        self.win.resize(1000, 600)
        self.win.setWindowTitle('HADES EYE')

# Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self.plt = self.win.addPlot(title="RF SPECTRUM ANALYZER")
        self.plt2 = self.win.addPlot(title="TRACKED SIGNAL")
        self.plt2.setLabel('right', 'Value')
        self.bufferSize = 1000
        self.data = np.zeros(self.bufferSize)
        self.curve = self.plt.plot()
        self.scatter = self.plt2.plot(pen=None, symbol='o', symbolPen=None)

        self.plt.setRange(xRange=[min, max], yRange=[-100, 0])
        self.plt2.setRange(xRange=[-5, 5], yRange=[-100, 0])
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.inter_maj)
        self.timer.start(20)
        self.locater = SigLocate()

    def inter_maj(self):
        rand = self.rf.pas()
        self.locater.update(rand)

        lim_data = np.linspace(self.min, self.max, len(rand))

        self.data = rand
        self.curve.setData(lim_data, self.data,)
        self.scatter.setData([self.locater.min])
        self.plt2.setLabel('bottom', str(self.locater.min))
        self.plt.setLabel('bottom', str(cal_dist(self.locater.min)))


if __name__ == '__main__':

    min, max = freq_parser(args.freq)

    if args.setup == "pp":
        rf = graphf_qt(False, min, max, args.mode)
    elif args.setup == "rt":
        rf = graphf_qt(True, min, max, args.mode)

# 840:900
