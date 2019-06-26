#script (python)
import json
import csv
import numpy as np

def id(x):
	print(str(x))

def main(prg):
	prg.ground([("base", [])])
	prg.solve()

	with open('stats.json', 'w') as fp:
		json.dump(prg.statistics, fp, sort_keys=True)
#end.