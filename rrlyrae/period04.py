"""
step 1: create text file organized in columns of time, light, error
step 2: create batch file for text file made above
step 3: use batch to run period04 and output a results file
step 4: parse results file for frequency, compare between .3 and 1
step 5: delete files made during execution and return
"""

import os
from os import path
import random
import string
from subprocess import check_output

def get_period(observations):
    print "{}".format(str(len(observations)))

    if len(observations) > 50:
        current_directory = os.getcwd()

        directory = path.join(current_directory, ".tmp")
        file_name = ''.join(random.choice(string.lowercase) for i in range(15))

        create_tmp_dir(directory)
        create_data_file(directory, file_name, observations)
        create_batch_file(directory, file_name)

        run_period04(directory, file_name)
        frequency = read_results_file(directory, file_name)

        clean_up(directory, file_name)

        result = 1 / frequency
        return result
    else:
        return 0.0

def create_tmp_dir(directory):
    if not path.isdir(directory):
        os.makedirs(directory)

def create_data_file(directory, file_name, observations):
    file_path = path.join(directory, file_name)
    file = open(file_path + ".dat", 'w+')
    for x in observations:
        file.write(str(x.to_tuple()[1]) + " " + str(x.to_tuple()[2]) + " " + str(x.to_tuple()[3]))
        file.write("\n")
    file.close()

def create_batch_file(directory, file_name):
    file_path = path.join(directory, file_name)
    bat_file = open(file_path + ".bat", 'w+')
    bat_file.write("import tou {0}.dat\n".format(path.abspath(file_path)))
    bat_file.write("fourier 0 20 o n\n")
    bat_file.write("savefreqs {0}.out\n".format(file_name))
    bat_file.write("exit\n")
    bat_file.close()

def run_period04(directory, file_name):
    file_path = path.join(directory, file_name)

    old_path = os.getcwd()
    os.chdir(directory)
    check_output(["period04","-batch={}.bat".format(file_name)])
    os.chdir(old_path)

def clean_up(directory, file_name):
    file_path = path.join(directory, file_name)

    dat_file = file_path + ".dat"
    bat_file = file_path + ".bat"
    out_file = file_path + ".out"

    os.remove(dat_file)
    os.remove(bat_file)
    os.remove(out_file)

def read_results_file(directory, file_name):
    file_path = path.join(directory, file_name)

    results_file = open(file_path + ".out", 'r')

    r = ""
    for line in results_file:
        r = line.split('\t')[1]
    results_file.close()

    return float(r)
