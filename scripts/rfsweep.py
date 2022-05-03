import subprocess
import numpy as np
from graphf import graphf
import argparse

parser = argparse.ArgumentParser(description='rf spectrum analyzer hackrf')
parser.add_argument('--setup', default="postprocessing", type=str,
                    help='realtime or postprocessing')




args = parser.parse_args()

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


def db_block(file_name, n=20, offset=0):
    db = []
    lines = file_to_list(file_name)
    for i in range(offset, n+offset):
        for x in lines[i][6]:
            db.append(x)

    return db


class rfsweep():
    def __init__(self, min=2400000000, max=2500000000, n=20):
        self.min = min
        self.max = max
        self.n = n*5
        self.g = graphf(self.min, self.max, self.n, -100, 0)
        self.phase = 0

        if args.setup=="realtime":
            self.setup = True
        else:
            self.setup = False

    def pas(self):
        if self.setup:
            bash_com("rm sample_rfsweep")
            bash_com("hackrf_sweep -f " + str(self.min/1000000) + ":" + str((self.max-10000000)/1000000) + " -r sample_rfsweep")

        if self.setup:
            self.g.update(db_block("sample_rfsweep", int(self.n/5), 0))

        else:    
            self.g.update(db_block("sample_rfsweep", int(self.n/5), self.phase*int(self.n/5)))

            
        self.phase += 1


rfsweep = rfsweep()

for i in range(0, 100):
    rfsweep.pas()
    