"""
Bo Wesdorp, bowesdorp@gmail.com
June, 2019, Universiteit van Amsterdam

This file contains code for running the Clingo algorithm.
"""
import os
import glob
import csv
import numpy as np
import json
import sys

if __name__ == '__main__':

    [argc, argv, windet, configuration] = sys.argv
    if argv != 'soc' and argv != 'soi' and argv != 'toc' and argv \
        != 'toi':
        print('Wrong input. Input can only be soc, soi, toc or toi.')

    labels = [
        'name',
        'n_candidates',
        'n_votes',
        'n_unique_votes',
        'acyc_edges',
        'complexity',
        'constraints',
        'constraints_binary',
        'constraints_ternary',
        'vars',
        'vars_eliminated',
        'vars_frozen',
        'atoms',
        'atoms_aux',
        'bodies',
        'bodies_tr',
        'count_bodies',
        'count_bodies_tr',
        'disjunctions',
        'disjunctions_non_hcf',
        'eqs',
        'eqs_atoms',
        'eqs_body',
        'eqs_others',
        'gammas',
        'rules',
        'rules_acyc',
        'rules_choice',
        'rules_heuristic',
        'rules_minimize',
        'rules_normal',
        'rules_tr',
        'rules_tr_acyc',
        'rules_tr_choice',
        'rules_tr_heuristic',
        'rules_tr_minimize',
        'rules_tr_normal',
        'sccs',
        'sccs_non_hcf',
        'sum_bodies',
        'sum_bodies_tr',
        'ufs_nodes',
        'choices',
        'conflicts',
        'conflicts_analyzed',
        'restarts',
        'restarts_last',
        'call',
        'concurrency',
        'cost',
        'exhausted',
        'models-enumerated',
        'models-optimal',
        'result',
        'signal',
        'cpu-time',
        'sat-time',
        'solve-time',
        'total-time',
        'unsat-time',
        'winner',
        ]

    result_output = 'results/clingo_' + configuration

    with open(result_output + '/' + argv + '.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(labels)

    mypath = os.getcwd()
    lp_files = glob.glob(mypath + '/voting_data/' + argv + '_p/*.lp')

    with open('data.json') as f:
        data_d = json.load(f)

    for file in lp_files:
        """Loop through all the voting settings."""
        string = 'clingo windet/' + windet + '.lp ' + 'stats.lp ' \
            + file \
            + ' -Wno-atom-undefined --project --time-limit=2000 --heuristic=' \
            + configuration
        print(string)
        os.system(string)

        name = file.split('/')[8].split('.')[0]

        # Store all statisctics
        all_stats = []
        try:
            with open('stats.json') as fp:
                datastore = json.load(fp)

            current = datastore['problem']['generator']
            for key in current:
                all_stats.append(current[key])

            current = datastore['problem']['lp']

            for key in current:
                all_stats.append(current[key])

            current = datastore['solving']['solvers']

            for key in current:
                all_stats.append(current[key])

            current = datastore['summary']

            for key in current:
                if key == 'models' or key == 'times':
                    for secondkey in current[key]:
                        all_stats.append(current[key][secondkey])
                else:
                    all_stats.append(current[key])

            os.remove('stats.json')
        except OSError as e:

            print('Process Killed')

        row = [name] + data_d[name] + all_stats

        with open(result_output + '/' + argv + '.csv', 'a') as \
            writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(row)
