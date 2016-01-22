/****************************
* CS470 Intro to AI
* Homework 4
* Problem 3 (a)
*
* 20130551 Youngjae Chang
*****************************/

/* Initial condition */
:- dynamic on/2.

on(a,b).
on(b,c).
on(c,table).

/* PART 1 : simple action scema */

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

/*
* [SWIPL log]
*
* ?- put_on(a, table).
* true 
* 
* ?- listing(on), listing(move).
* :- dynamic on/2.
* 
* on(b, c).
* on(c, table).
* on(a, table).
* 
* :- dynamic move/3.
* 
* move(a, b, table).
* 
* true.
* 
* ?- put_on(c,a).
* false.
* 
* ?- put_on(a, table), put_on(c,a).
* true.
*/


/* PART 2: recursive action */

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

/*
* [SWIPL log]
*
* ?- r_put_on(c,a).
* true .
* 
* ?- listing(on), listing(move).
* :- dynamic on/2.
* 
* on(a, table).
* on(b, table).
* on(c, a).
* 
* :- dynamic move/3.
* 
* move(a, b, table).
* move(b, c, table).
* move(c, table, a).
* 
* true.
*/


/* PART 3: planning problem */

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

/*
* [SWIPL log] -- 1
*
* ?- do([on(a,table),on(b,a),on(c,b)]).
* true .
* 
* ?- listing(on), listing(move).
* :- dynamic on/2.
* 
* on(a, table).
* on(b, a).
* on(c, b).
* 
* :- dynamic move/3.
* 
* move(a, b, table).
* move(b, c, a).
* move(c, table, b).
* 
* true.
*/

/*
* [SWIPL log] -- 2
*
* ?- do([on(c,b),on(b,a),on(a,table)]).
* true .
* 
* ?- listing(on), listing(move).
* :- dynamic on/2.
* 
* on(a, table).
* on(b, a).
* on(c, b).
* 
* :- dynamic move/3.
* 
* move(a, b, table).
* move(b, c, table).
* move(c, table, b).
* move(c, b, table).
* move(b, table, a).
* move(c, table, b).
* 
* true.
*/

/*
* [SWIPL log] -- 3
*
* ?- do([on(a,b),on(b,a)]).
* ^CAction (h for help) ? abort
* % Execution Aborted
* ?- listing(move).
* ...
* move(a, b, table).
* move(b, table, a).
* move(b, a, table).
* move(a, table, b).
* ...                       // infinite repetition
*
* true.
*/
