"""
Bo Wesdorp, bowesdorp@gmail.com
June, 2019, Universiteit van Amsterdam

This file contains code that converts the results of the Clingcon
algorithm to one single .csv file.
"""

import re
import sys
import os
import glob
import csv

count = 0
files_loc = glob.glob(os.getcwd()
                      + '/results/clingcon/results_clingcon_toi/*.txt')
labels = [
    'Name',
    'Solve',
    'CPU',
    'Choices',
    'Conflicts',
    'Backtrack',
    'Restarts',
    ]

# Create new file .csv file
with open(os.getcwd() + '/results/clingcon/toi.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(labels)

for file in files_loc:
    data = []
    name = file.split('/')[9].split('.')[0]
    print name
    with open(file, 'r') as fp:
        for line in fp:
            if 'Choices' in line:
                data.append(float(re.findall('\d+', line)[0]))
            elif 'Conflicts' in line:
                data.append(float(re.findall('\d+', line)[0]))
                data.append(float(re.findall('\d+', line)[1]))
            elif 'Restarts' in line:
                data.append(float(re.findall('\d+', line)[0]))
            elif 'CPU Time' in line:
                data.append(float(re.findall("\d+\.\d+", line)[0]))
            elif 'Time' in line:
                data.append(float(re.findall("\d+\.\d+", line)[1]))

    with open(os.getcwd() + '/results/clingcon/toi.csv', 'a') as \
        writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([name] + data)
