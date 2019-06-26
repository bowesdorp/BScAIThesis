
"""
Bo Wesdorp, bowesdorp@gmail.com
June, 2019, Universiteit van Amsterdam

This file contains code for the main code for applying the Clingcon algorithm
on the voting data.
"""

import os
import glob
import csv
import numpy as np
import json
import sys

if __name__ == '__main__':
    [argc, argv, windet] = sys.argv

    mypath = os.getcwd()
    lp_files = glob.glob(mypath + '/voting_data/' + argv + '_p/*.lp')

    dirname = mypath + '/results/clingcon'
    try:
        os.mkdir(dirname)
    except FileExistsError:
        print ()

    dirname = dirname + '/' + argv
    try:
        os.mkdir(dirname)
    except FileExistsError:
        print ()

    # Loop through all voting settings and compute winner.
    for file in lp_files:
        name = file.split('/')[8].split('.')[0]
        txt_file = dirname + '/' + name + '.txt'
        f = open(txt_file, 'w+')
        string = \
            './algorithms/clingcon-3.3.0 -Wno-atom-undefined ~/Documents/Afstudeerscriptie/ja-asp/windet/' \
            + windet + '.lp ' + file + ' --time-limit=2000' + ' -s>' \
            + txt_file
        print(string)
        os.system(string)
