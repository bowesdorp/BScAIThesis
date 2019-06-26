%%% BASIC ENCODING OF THE WINNER DETERMINATION PROBLEM

#include "../ja.lp".

% generate a collective outcome
agent(col).

% auxiliary predicate to refer to the collective outcome
collective(X) :- js(col,X), ilit(X).

% show only the collective outcome

winner(A) :- candidate(A), collective(p(A,B)) : candidate(B), A != B.

#show winner/1.

#script (python)
import json

def id(x):
	print(str(x))

def main(prg):
	prg.ground([("base", [])])
	prg.solve()

	with open('stats.json', 'w') as fp:
		json.dump(prg.statistics, fp, sort_keys=True)
#end.