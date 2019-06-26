import os, glob
import csv
import numpy as np
import json
import sys

if __name__ == "__main__":
	[argc, argv, windet] = sys.argv

	mypath = os.getcwd()
	lp_files = glob.glob(mypath + '/' + argv + '_p/*.lp')
	dirname = mypath+"/results_wasp"
	os.mkdir(dirname)
	for file in lp_files:
		name = file.split('/')[7].split('.')[0]
		txt_file = dirname+'/'+name+".txt"

		print(txt_file)
		f= open(txt_file,"w+")
		string = "gringo ~/Documents/Afstudeerscriptie/ja-asp/windet/" + windet + ".lp " + file + " --output=smodels | ~/Desktop/alviano-wasp-2c1bda3/build/stats/wasp --stats=2 2>"+txt_file
		print(string)
		os.system(string)