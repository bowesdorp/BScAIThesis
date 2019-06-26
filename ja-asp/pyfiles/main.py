"""
Bo Wesdorp, bowesdorp@gmail.com
June, 2019, Universiteit van Amsterdam

This file contains code for the main system to run the algorithms.
"""

import run_clingo
import process_data
import sys
import os
import glob
import shutil

if __name__ == '__main__':
    [argc, argv, windet, solver, config] = sys.argv
    if argv != 'soc' and argv != 'soi' and argv != 'toc' and argv \
        != 'toi' and argv != 'all':

        print('Wrong input. Input can only be soc, soi, toc, toi or all.')
    else:
        if argv == 'all':
            print('Converting files....')
            os.system('python pyfiles/process_data.py soc')
            print('All files converted.')
        else:
            print('Converting files....')
            os.system('python pyfiles/process_data.py ' + argv)
            print("All files converted.")

        try:
            os.mkdir('results')
        except FileExistsError:
            print('Calculating')

        try:
            if solver == 'clingcon':
                os.mkdir('results/' + solver)
            else:
                os.mkdir('results/' + solver + '_' + config)
        except FileExistsError:
            print()

        if solver == 'clingo':
            """ Apply Clingo with the specified decision heurtistic 
            on the voting data."""
            if argv == 'all':
                os.system('python pyfiles/run_clingo.py soc ' + windet
                          + ' ' + config)
                os.system('python pyfiles/process_data.py toc')
                os.system('python pyfiles/run_clingo.py toc ' + windet
                          + ' ' + config)
                os.system('python pyfiles/process_data.py soi')
                os.system('python pyfiles/run_clingo.py soi ' + windet
                          + ' ' + config)
                os.system('python pyfiles/process_data.py toi')
                os.system('python pyfiles/run_clingo.py toi ' + windet
                          + ' ' + config)
            else:
                os.system('python pyfiles/run_clingo.py ' + argv + ' '
                          + windet + ' ' + config)
        elif solver == 'clingcon':
            """ Apply Clingcon on the voting data."""
            if argv == 'all':
                os.system('python pyfiles/run_clingcon.py soc '
                          + windet)
                os.system('python pyfiles/process_data.py toc')
                os.system('python pyfiles/run_clingcon.py toc '
                          + windet)
                os.system('python pyfiles/process_data.py soi ')
                os.system('python pyfiles/run_clingcon.py soi '
                          + windet)
                os.system('python pyfiles/process_data.py toi')
                os.system('python pyfiles/run_clingcon.py toi '
                          + windet)
            else:
                os.system('python pyfiles/run_clingcon.py ' + argv + ' '
                           + windet + ' ' + config)

    os.remove("data.json")
