/*
* State Encoding
*
* Representation of each individuals.
*   Missionaries
*   -- -- --
*   M1 M2 M3 C1 C3 C3 Boat
*            -- -- --
*            Cannibals
*
* Position of each people comrise a lsit.
*     M1 M2 M3 C1 C2 C3 Boat
*   [ l, l, r, l, l, r, l ]  <-- state encoding
*/

/*
* State Encoding
*
* Configuration of Left Bank:
* [m, m, m]
* [c, c, c]
* [b]
*/

state([M,C]) :-
    missionaries(M),
    cannibals(C).
missionaries([m,m,m]).
missionaries([m,m]).
missionaries([m]).
missionaries([]).
cannibals([c,c,c]).
cannibals([c,c]).
cannibals([c]).
cannibals([]).

/* follows (in, in) : bool */
follows([A,B,[b]], [X,Y,[]]) :-
    state([A,B]), state([X,Y]),
    leave([A,B],[X,Y]).
follows([A,B,[]], [X,Y,[b]]) :-
    state([A,B]), state([X,Y]),
    leave([X,Y],[A,B]).

leave([A,B],[X,Y]) :- A == [m | X],    B == [c | Y].
leave([A,B],[X,Y]) :- A == [m, m | X], B == Y.
leave([A,B],[X,Y]) :- A == X,          B == [c, c | Y].
leave([A,B],[X,Y]) :- A == [m | X],    B == Y.
leave([A,B],[X,Y]) :- A == X,          B == [c | Y].

l([A,B],[X,Y]) :- append(X,[m],A), B == append(Y,[c],B).

/* admissible (in) : bool */
admissible([M,C,_]) :-
    length(M, Mnum), length(C, Cnum),
    0 =< Mnum, Mnum =< 3,
    0 =< Cnum, Cnum =< 3,
    adm_helper(Mnum, Cnum),
    Mnum2 is 3 - Mnum,
    Cnum2 is 3 - Cnum,
    adm_helper(Mnum2, Cnum2).
adm_helper(Mnum,_) :- Mnum == 0.
adm_helper(Mnum,Cnum) :- Mnum >= Cnum.

/* plan (in, in, out) */
plan(S,S,[]).
plan(X,G,[X]) :-
    follows(X,G).
plan(X,G,L) :-
    follows(S, G),
    admissible(S),
    plan(X,S,P),
    not(member(S, P)),
    L == [S | P].
