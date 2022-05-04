import subprocess


def log(msg, file):
    with open(file, "a") as f:
        f.write(msg+"\n")
    f.close()


def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


def bash_com(cmd="ls"):  # -r sample
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
