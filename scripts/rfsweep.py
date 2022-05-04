import subprocess
from importlib_metadata import files
import numpy as np
from graphf import graphf
import argparse

parser = argparse.ArgumentParser(description='rf spectrum analyzer hackrf')
parser.add_argument('--setup', default="postprocessing", type=str,
                    help='realtime or postprocessing')
parser.add_argument("--qt", default=False, type=bool, help="use qt")


args = parser.parse_args()


def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


def bash_com(cmd="hackrf_sweep -f 2400:2490"):  # -r sample
    bashCmd = cmd.split(" ")
    process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)

    output, error = process.communicate()

    if not error:
        return output
    else:
        return error


def file_to_list(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')
        lines[i] = lines[i].split(', ')
        for j in range(2, len(lines[i])):
            lines[i][j] = float(lines[i][j])
        var = lines[i][0:6]
        var.append(lines[i][len(lines[i])-5: len(lines[i])])
        lines[i] = var
    return lines


def db_block(lines, n=20, offset=0, min=2400000000):
    db = [0 for i in range(int(n*5))]

    for i in range(offset, n+offset):
        for t, x in enumerate(lines[i][6]):

            db[int(((int(lines[i][2])-min)/1000000)+t)] = x

    return db


class rfsweep():
    def __init__(self, setup=False, min=2400000000, max=2500000000, qt=False):
        n = int((max-min)/1000000*0.2)  # de base c 20
        self.min = min
        self.max = max
        self.n = n*5
        if qt:
            # a changer vers un qt graph
            self.g = graphf(min, max, n, "hackrf_sweep")
        else:
            self.g = graphf(self.min, self.max, self.n, -100, 0)
        self.phase = 0

        self.setup = setup
        if not checkFileExistance("sample_rfsweep"):
            bash_com("touch sample_rfsweep")

        self.sample = file_to_list("sample_rfsweep")

    def pas(self):
        if self.setup:
            bash_com("rm sample_rfsweep")
            bash_com("hackrf_sweep -1 -f " + str(int(self.min/1000000)) + ":" +
                     str(int((self.max-10000000)/1000000)) + " -r sample_rfsweep")

        if self.setup:
            self.sample = file_to_list("sample_rfsweep")
            self.g.update(db_block(self.sample, int(self.n/5), 0))

        else:
            self.g.update(db_block(self.sample, int(
                self.n/5), self.phase*int(self.n/5), self.min))

        self.phase += 1


rfsweep = rfsweep()

for i in range(0, 100):
    rfsweep.pas()
