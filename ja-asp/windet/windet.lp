%%% BASIC ENCODING OF THE WINNER DETERMINATION PROBLEM

#include "../ja.lp".

% generate a collective outcome
agent(col).

% auxiliary predicate to refer to the collective outcome
collective(X) :- js(col,X), ilit(X).

% show only the collective outcome

winner(A) :- candidate(A), collective(p(A,B)) : candidate(B), A != B.

#show winner/1.