"""
Bo Wesdorp, bowesdorp@gmail.com
June, 2019, Universiteit van Amsterdam

This file contains code for converting the data from PrefLib to Logic Programmes.
"""

import os
import glob
import shutil
import json
import sys
import re
from itertools import permutations


def parse_file(file_name):
    """This function receives a voting setting as input and returns 
    all the relevant data."""
    f = open(file_name, 'r')
    count = 0
    data = []
    for line in f:
        if count is 0:
            n_candidates = int(line)
        elif count == n_candidates + 1:
            n_voters = int(line.rstrip().split(',')[0])
            unique_votes = int(line.rstrip().split(',')[2])
        elif count > n_candidates + 1:
            data.append(line.rstrip().split(','))
        count += 1
    return [n_candidates, n_voters, unique_votes, data]



def create_file(data_array, name, filetype):
    """This is the main function for converting the Preflib data
    to a logic programme."""
    [n_cand, n_vote, unique_votes, data] = data_array

    if false_data(data):
        return

    # Filter away the too complex voting settings
    if n_cand > 200 or unique_votes > 1000:
        return

    f = open('voting_data/' + filetype + '_p/' + name + '.lp', 'w')
    f.write("candidate(1.." + str(n_cand) + ").\n")
    f.write("issue(p(X,Y)) :- candidate(X), candidate(Y), X != Y.\n")
    f.write("clause(c(1,X,Y),(p(X,Y);p(Y,X))) :- candidate(X), candidate(Y), X != Y.\n")
    f.write("clause(c(2,X,Y),(-p(X,Y);-p(Y,X))) :- candidate(X), candidate(Y), X != Y.\n")
    f.write("clause(c(3,X,Y,Z),(-p(X,Y);-p(Y,Z);p(X,Z))) :- candidate(X), candidate(Y), candidate(Z), X != Y, Y != Z, X != Z.\n\n")
    f.write("voter(1.." + str(n_vote) + ").\n")

    # Loop through all ballots
    current_voter = 1
    for ballot in data:
        voter_n = ballot[0]
        string = 'js((' + str(current_voter) + '..' + str(int(voter_n)
                - 1 + current_voter) + '),('
        current_voter += int(voter_n)

        if filetype == 'soc':
            preferences = soc_file(ballot)
        elif filetype == 'toc':

            preferences = toc_file(ballot)
        elif filetype == 'soi':

            preferences = soi_file(ballot, n_cand)
        elif filetype == 'toi':

            preferences = toi_file(ballot, n_cand)

        for pref in preferences:
            string += 'p(' + str(int(pref[0])) + ',' \
                + str(int(pref[1])) + ');'

        f.write(string[:len(string) - 1] + ')).\n')

def false_data(data):
    """This function checks if the voting setting is a voting setting
    where voters are only allowed to vote once for each candidate."""
    for ballot in data:
        ballot = ballot[1:]
        str1 = ' '.join(ballot)
        list_of_nums = list(map(int, re.findall(r"\d+", str1)))
        if len(list_of_nums) > len(set(list_of_nums)):
            return True
    return False


def remove_brackets(ballot):
    """This function removes the brackets in the TOC and TOI data-sets."""
    temp = ballot[1:]
    if '{}' in temp:
        temp.remove('{}')

    for k in range(len(temp)):
        cur = temp[k]
        if '{' in cur and '}' in cur:
            temp[k] = cur[1:len(cur) - 1]

    for j in range(len(temp)):
        if '{' in temp[j]:
            temp[j] = (temp[j])[1:]
        elif '}' in temp[j]:
            temp[j] = (temp[j])[:len(temp[j]) - 1]
    return temp


def complete_ballot(preference, candidates):
    """This function checks the ballot on validness."""
    if len(preference) == candidates:
        return True
    return False


def soc_file(ballot):
    """Converts a SOC ballot to all preferences."""
    combination = []
    preference = ballot[1:]
    temp = preference[1:]
    for i in range(len(preference) - 1):
        for j in range(len(temp)):
            combination.append((preference[i], temp[j]))
        temp = temp[1:]
    return combination

def soi_file(ballot, candidates):
    """Converts a SOI ballot to all preferences."""
    preference = ballot[1:]
    if complete_ballot(preference, candidates):
        return soc_file(ballot)
    
    # If the ballot is missing votes convert all known preferences. 
    else: 
        cand_list = [str(x) for x in list(range(1, candidates + 1))]
        soi_comb = soc_file(ballot)
        for pref in preference:
            for cand in cand_list:
                if cand not in preference:
                    soi_comb.append((pref, cand))
        return soi_comb

def toi_file(ballot, candidates):
    """Converts a TOI ballot to all preferences."""
    preference = ballot[1:]
    if complete_ballot(preference, candidates):
        return toc_file(ballot)
    else:
        toc = toc_file(ballot)
        soi = soi_file(remove_brackets([0] + ballot), candidates)
        return list(set(soi + toc))


def toc_file(ballot):
    """Converts a TOC ballot to all preferences."""
    preference = ballot[1:]
    temp = preference

    if '{}' in preference:
        preference.remove('{}')
    mylist = list(dict.fromkeys(temp))

    # Make all possible combinations between the ties.
    for k in range(len(preference)):
        cur = preference[k]
        if '{' in cur and '}' in cur:
            preference[k] = cur[1:len(cur) - 1]
    i = 0
    all_ties = []
    while i < len(preference):
        ties = []
        if '{' in preference[i]:
            current = preference[i]
            ties.append(current[1:])
            i += 1
            current = preference[i]
            while '}' not in current:
                ties.append(current)
                i += 1
                current = preference[i]
            ties.append(current[:len(current) - 1])
            perm = list(permutations(ties, 2))
            all_ties += perm
        i += 1
    temp = remove_brackets(ballot)

    # Get all strict order preferences
    combination = soc_file([0] + temp)

    if all_ties != []:
        all_combs = list(set(combination + all_ties))
    else:
        all_combs = combination
    return all_combs


def make_dir(filetype):
    """This function creates a new file for the processed data files."""
    dirName = os.getcwd() + '/voting_data/' + filetype + '_p'
    try:
        os.mkdir(dirName)
        print ('Directory ', dirName, ' Created ')
    except FileExistsError:
        shutil.rmtree(dirName)
        print ('Directory ', dirName, ' Created ')
        os.mkdir(dirName)


if __name__ == '__main__':
    """Main script to run the data processing."""
    [argc, argv] = sys.argv
    if argv != 'soc' and argv != 'soi' and argv != 'toc' and argv \
        != 'toi' and argv != 'all':
        print('Wrong input. Input can only be soc, soi, toc or toi.')
        
    else:
        make_dir(argv)
        print(argv)
        files = glob.glob(os.getcwd() + '/voting_data/' + argv + '/*.'
                          + argv)
        data_dict = {}
        for file_name in files:
            name = file_name.split('/')[8].split('.')[0]

            parsed_data = parse_file(file_name)
            create_file(parsed_data, name, argv)

            data_dict[name] = parsed_data[:3]

        with open('data.json', 'w') as fp:
            json.dump(data_dict, fp, sort_keys=True, indent=4)
