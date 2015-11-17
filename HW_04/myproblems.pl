/****************************
* CS470 Intro to AI
* Homework 4
* Problem 3 (b)
*
* 20130551 Youngjae Chang
*****************************/

/* solver */
:- dynamic on/2

put_on(A,B) :-
    A \== table,
    A \== B,
    on(A,X),
    clear(A),
    clear(B),
    retract(on(A,X)),
    assert(on(A,B)),
    assert(move(A,X,B)).

clear(table).
clear(B) :-
    not(on(_X,B)).

r_put_on(A,B) :-
    on(A,B).
r_put_on(A,B) :-
    not(on(A,B)),
    A \== table,
    A \== B,
    clear_off(A),
    clear_off(B),
    on(A,X),
    retract(on(A,X)),
    assert(on(A,B)),
    assert(move(A,X,B)).

clear_off(table).
clear_off(A) :-
    not(on(_X,A)).
clear_off(A) :-
    A \== table,
    on(X,A),
    clear_off(X),
    retract(on(X,A)),
    assert(on(X,table)),
    assert(move(X,A,table)).

do(Glist) :-
    valid(Glist),
    do_all(Glist,Glist).

valid(_).

do_all([G|R],Allgoals) :-
    call(G),
    do_all(R,Allgoals),!.
do_all([G|_],Allgoals) :-
    achieve(G),
    do_all(Allgoals,Allgoals).
do_all([],_Allgoals).

achieve(on(A,B)) :-
    r_put_on(A,B).


/* PROBELM #1 */
problem01() :-
    /* init */
    assert(on(a,b)),
    assert(on(b,c)),
    assert(on(c,d)),
    assert(on(d,table)),
    /* goal */
    do([on(d,c),on(c,b),on(b,a),on(a,table)]),
    listing(move).
/* swipl log
* ?- problem01.
* :- dynamic move/3.
*
* move(a, b, table).
* move(b, c, table).
* move(c, d, table).
* move(d, table, c).
* move(d, c, table).
* move(c, table, b).
* move(d, table, c).
* move(d, c, table).
* move(c, b, table).
* move(b, table, a).
* move(d, table, c).
* move(d, c, table).
* move(c, table, b).
* move(d, table, c).
*
* true .
*/


/* PROBLEM #2*/
problem02() :-
    /* init */
    assert(on(a,b)),
    assert(on(b,table)),
    assert(on(c,d)),
    assert(on(d,table)),
    /* goal */
    do([on(a,c),on(c,table),on(b,d),on(d,table)]),
    listing(move).
/* swipl log
* ?- problem02.
* :- dynamic move/3.
* 
* move(a, b, c).
* move(a, c, table).
* move(c, d, table).
* move(a, table, c).
* move(b, table, d).
* 
* true .
*/
