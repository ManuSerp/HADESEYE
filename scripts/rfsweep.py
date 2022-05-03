import subprocess
import numpy as np
import graphf


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


def db_block(file_name, n=20):
    db = []
    lines = file_to_list(file_name)
    for i in range(n):
        for x in lines[i][6]:
            db.append(x)
    g = graphf.graphf()
    g.update(db)


db_block("sample")
