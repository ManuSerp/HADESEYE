from importlib_metadata import files
import numpy as np
from sympy import li
from rfsweep_lib.graphf import graphf
from rfsweep_lib.subfun import *
import argparse
import datetime

parser = argparse.ArgumentParser(description='rf spectrum analyzer hackrf')
parser.add_argument('--setup', default="pp", type=str,
                    help='realtime or postprocessing')
parser.add_argument("--qt", default=False, type=bool, help="use qt")
parser.add_argument("--freq", default="2400:2500", type=str, help="freq range")


args = parser.parse_args()


def db_block(lines, n=20, offset=0, min=2400000000, mode=0):
    db = [0 for i in range(int(n*5))]

    for i in range(offset, n+offset):
        for t, x in enumerate(lines[i][6]):

            if mode == 1:
                if x > -50:
                    db[int(((int(lines[i][2])-min)/1000000)+t)] = x
                else:
                    db[int(((int(lines[i][2])-min)/1000000)+t)] = -50
            else:

                db[int(((int(lines[i][2])-min)/1000000)+t)] = x

    return db


class rfsweep():
    def __init__(self, setup=False, min=2400000000, max=2500000000, qt=False, mode=0):
        n = int((max-min)/1000000*0.2)  # de base c 20
        self.min = min
        self.max = max
        self.n = n*5
        self.qt = qt
        self.mode = mode

        if not self.qt:
            self.g = graphf(self.min, self.max, self.n, -100, 0)
        self.phase = 0

        self.setup = setup
        if not checkFileExistance("rfsweep/rfsweep_data/sample_rfsweep"):
            bash_com("touch rfsweep/rfsweep_data/sample_rfsweep")

        self.sample = file_to_list("rfsweep/rfsweep_data/sample_rfsweep")

    def pas(self):
        init = datetime.datetime.now()
        if self.setup:
            bash_com("rm rfsweep/rfsweep_data/sample_rfsweep")
            bash_com("hackrf_sweep -1 -f " + str(int(self.min/1000000)) + ":" +
                     str(int((self.max-10000000)/1000000)) + " -r rfsweep/rfsweep_data/sample_rfsweep > /dev/null")

            self.sample = file_to_list("rfsweep/rfsweep_data/sample_rfsweep")

            if self.qt:
                print(delta_micro(init, datetime.datetime.now()))
                return(db_block(self.sample, int(self.n/5), 0, self.min, self.mode))
            else:
                self.g.update(
                    db_block(self.sample, int(self.n/5), 0, self.min))
        else:
            if self.qt:
                var = db_block(self.sample, int(
                    self.n/5), self.phase*int(self.n/5), self.min)
                self.phase += 1
                print(delta_micro(init, datetime.datetime.now()))
                return var

            else:
                self.g.update(db_block(self.sample, int(
                    self.n/5), self.phase*int(self.n/5), self.min))

        self.phase += 1
        end = datetime.datetime.now()
        print(delta_micro(init, end))

    def load_sample(self, file_name):
        self.sample = file_to_list(file_name)


if __name__ == '__main__':
    min, max = freq_parser(args.freq)

    if args.setup == "pp":
        rf = rfsweep(False, min, max, args.qt)
        for i in range(0, int(len(rf.sample)/(rf.n/5))):
            rf.pas()

    elif args.setup == "rt":
        rf = rfsweep(True, min, max, args.qt)
        for i in range(0, 1000):
            rf.pas()

# rfsweep.load_sample("rfsweep/rfsweep_data/sample_rfsweep")
