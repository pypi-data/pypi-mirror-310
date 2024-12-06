def length():
    string =  """
        list_length([], 0).
        list_length([_ | L], N) :-
            list_length(L, N1),
            N is N1 + 1. 
    """
    
    print(string)
    
def is_member():
    string =  """
        is_member(X, [X | _]) :- !.
 
        is_member(X, [_ | Rest]) :-    
            is_member(X, Rest).
    """
    
    print(string)
    
def append_l2_end_l1():
    string =  """
        append_list([], L2, L2).    

        append_list([X | L1], L2, [X | L3]) :-
            append_list(L1, L2, L3).
    """
    
    print(string)
    
def delete_element():
    string =  """
        % Deletion of any element from empty list will produce empty list(base case)
        delete_element(_, [], []).    

        delete_element(X, [X | L], L) :- !.

        delete_element(X, [Y | L], [Y | L1]) :-
            delete_element(X, L, L1).
    """
    
    print(string)
    
def sum_n():
    string =  """
        sum_n(0, 0).    

        sum_n(N, Sum) :-
            N > 0,
            N1 is N - 1,
            sum_n(N1, Sum1),
            Sum is Sum1 + N.
    """
    
    print(string)
    
def sum_list():
    string =  """
        sum_list([], 0).    

        sum_list([X | L], S) :-
            sum_list(L, S1),
            S is S1 + X.
    """
    
    print(string)
    
def reverse_list():
    string =  """
        reverse_list([], []).    

        reverse_list([X | L], Rev) :-
            reverse_list(L, RevL),
            append_list(RevL, [X], Rev).
    """
    
    print(string)
    
def sumOfDigits():
    string =  """
        sumOfDigits(0, 0).    

        sumOfDigits(N, Sum) :-
            N > 0,
            D in N mod 10,
            N1 is N // 10,
            sumOfDigits(N1, Sum1),
            Sum is Sum1 + D.
    """
    
    print(string)
    
def factorial():
    string =  """
        factorial(0, 1).    

        factorial(N, F) :-
            N > 0,
            N1 is N - 1,
            factorial(N1, F1),
            F is N * F1.
    """
    
    print(string)
    
def fibonacci():
    string =  """
        fibonacci(0, 0).    

        fibonacci(1, 1).    

        fibonacci(N, F) :-
            N > 1,
            N1 is N - 1,
            N2 is N - 2,
            fibonacci(N1, F1),
            fibonacci(N2, F2),
            F is F1 + F2.
    """
    
    print(string)
    
def permutation():
    string =  """
        permutation([], []).    

        permutation(L, [X | P]) :-
            select(X, L, L1),
            permutation(L1, P).
    """
    
    print(string)
    
def gcd():
    string =  """
        gcd(0, N, N) :- 
            N > 0, !.    

        gcd(M, N, G) :- 
            M >= N, 
            M1 is M - N, 
            gcd(M1, N, G).    

        gcd(M, N, G) :- 
            M < N, 
            gcd(N, M, G).
    """
    
    print(string)
    
def subset():
    string =  """
        subset([], []).    

        subset([X | L], [X | S]) :-
            subset(L, S).    

        subset([_ | L], S) :-
            subset(L, S).
    """
    
    print(string)
    
def quicksort():
    string =  """
        quicksort([], []).    

        quicksort([X | L], S) :-
            partition(X, L, L1, L2),
            quicksort(L1, S1),
            quicksort(L2, S2),
            append_list(S1, [X | S2], S).    

        partition(_, [], [], []).    

        partition(X, [Y | L], [Y | L1], L2) :-
            X > Y,
            partition(X, L, L1, L2).    

        partition(X, [Y | L], L1, [Y | L2]) :-
            X =< Y,
            partition(X, L, L1, L2).
    """
    
    print(string)
    
def merge_sort():
    string =  """
        merge_sort([], []).    

        merge_sort([X], [X]).    

        merge_sort(L, S) :-
            L = [_, _ | _],
            divide(L, L1, L2),
            merge_sort(L1, S1),
            merge_sort(L2, S2),
            merge(S1, S2, S).    

        divide([], [], []).    

        divide([X], [X], []).    

        divide([X, Y | L], [X | L1], [Y | L2]) :-
            divide(L, L1, L2).    

        merge(L, [], L).    

        merge([], L, L).    

        merge([X | L1], [Y | L2], [X | L]) :-
            X =< Y,
            merge(L1, [Y | L2], L).    

        merge([X | L1], [Y | L2], [Y | L]) :-
            X > Y,
            merge([X | L1], L2, L).
    """
    
    print(string)
    
def pallindrome():
    string =  """
        pallindrome(L) :-
            reverse_list(L, L).
    """
    
    print(string)
    
def flatten():
    string =  """
        flatten_list([], []).                % Base case: an empty list is already flattened.
        flatten_list([H|T], Flat) :- 
            is_list(H),                      % If the head is a list,
            flatten_list(H, FlatH),          
            flatten_list(T, FlatT),          
            append(FlatH, FlatT, Flat).      % Append the flattened head and tail.
        flatten_list([H|T], [H|FlatT]) :- 
            \+ is_list(H),                   % If the head is not a list,
            flatten_list(T, FlatT).          % Just recurse on the tail.

    """
    
    print(string)
    
def add():
    string =  """
        add(0, Y, Y).    

        add(s(X), Y, s(Z)) :-
            add(X, Y, Z).
    """
    
    print(string)
    
def multiply():
    string =  """
        multiply(0, _, 0).    

        multiply(s(X), Y, Z) :-
            multiply(X, Y, Z1),
            add(Z1, Y, Z).
    """
    
    print(string)
    
def power():
    string =  """
        power(_, 0, s(0)).    

        power(X, s(Y), Z) :-
            power(X, Y, Z1),
            multiply(Z1, X, Z).
    """
    
    print(string)
    
    
def merge_sort1():
    string =  """
        merge_sorted([], L, L).       % Base case: merging with an empty list results in the other list.
    merge_sorted(L, [], L).       % Base case: merging with an empty list results in the other list.
    merge_sorted([H1|T1], [H2|T2], [H1|T]) :- 
        H1 =< H2,                % If the head of the first list is smaller or equal,
        merge_sorted(T1, [H2|T2], T).  % Include it and recurse on the tail of the first list.
    merge_sorted([H1|T1], [H2|T2], [H2|T]) :-
        H1 > H2,                 % If the head of the second list is smaller,
        merge_sorted([H1|T1], T2, T).  % Include it and recurse on the tail of the second list.
    """
    
    print(string)
    
def ex1():
    string =  """
        directlyin(katrina,olga).
        directlyin(olga,natsha).
        directlyin(natsha,irina).

        in(X,Y) :- directlyin(X,Y).
        in(X,Y) :- directlyin(X,Z) , in(Z,Y).
    """
    
    print(string)
    
def ex2():
    string =  """
        greater_than(succ(X),X).
        greater_than(succ(X),Y) :- greater_than(X,Y).
    """
    
    print(string)

def ex3():
    string =  """
        directTrain(forbach,saarbruecken).
        directTrain(freyming,forbach).
        directTrain(fahlquemont,stAvold).
        directTrain(stAvold,forbach).
        directTrain(saarbruecken,dudweiler).
        directTrain(metz,fahlquemont).
        directTrain(nancy,metz).

        travelBetween(X,Y) :- directTrain(X,Y).
        % travelBetween(X,Y) :- directTrain(Y,X).

        travelBetween(X,Y) :- directTrain(X,Z),travelBetween(Z,Y).
        travelBetween(X,Y) :- directTrain(Y,Z),travelBetween(Z,X).
    """
    
    print(string)
    
def ex4():
    string =  """
        byCar(auckland,hamilton).
        byCar(hamilton,raglan).
        byCar(valmont,saarbruecken).
        byCar(valmont,metz).
        byTrain(metz,frankfurt).
        byTrain(saarbruecken,frankfurt).
        byTrain(metz,paris).
        byTrain(saarbruecken,paris).
        byPlane(frankfurt,bangkok).
        byPlane(frankfurt,singapore).
        byPlane(paris,losAngeles).
        byPlane(bangkok,auckland).
        byPlane(losAngeles,auckland).


        travel(X,Y) :- (byCar(X,Y);byPlane(X,Y);byTrain(X,Y)).

        travel(X,Y) :- (byCar(X,Z) ; byPlane(X,Z) ; byTrain(X,Z)) , travel(Z,Y).
    """
    
    print(string)
    
def ex5():
    string =  """
        connected(1,2).
        connected(3,4).
        connected(5,6).
        connected(7,8).
        connected(9,10).
        connected(12,13).
        connected(13,14).
        connected(15,16).
        connected(17,18).
        connected(19,20).
        connected(4,1).
        connected(6,3).
        connected(4,7).
        connected(6,11).
        connected(14,9).
        connected(11,15).
        connected(16,12).
        connected(14,17).
        connected(16,19).

        path(X,Y) :- connected(X,Y).
        path(X,Y) :- connected(X,Z) , path(Z,Y).
    """
    
    print(string)
    
def ex6():
    string = """
        byCar(auckland,hamilton).
        byCar(hamilton,raglan).
        byCar(valmont,saarbruecken).
        byCar(valmont,metz).
        byTrain(metz,frankfurt).
        byTrain(saarbruecken,frankfurt).
        byTrain(metz,paris).
        byTrain(saarbruecken,paris).
        byPlane(frankfurt,bangkok).
        byPlane(frankfurt,singapore).
        byPlane(paris,losAngeles).
        byPlane(bangkok,auckland).
        byPlane(losAngeles,auckland).


        travel(X, Y, go(X,Y)) :- (byCar(X,Y);byPlane(X,Y);byTrain(X,Y)).

        travel(X,Y, go(X, Z, Route)) :- (byCar(X,Z) ; byPlane(X,Z) ; byTrain(X,Z)) , travel(Z,Y, Route).
            
    """
    
    print(string)

def ex7():
    string = """
        byCar(auckland,hamilton).
        byCar(hamilton,raglan).
        byCar(valmont,saarbruecken).
        byCar(valmont,metz).
        byTrain(metz,frankfurt).
        byTrain(saarbruecken,frankfurt).
        byTrain(metz,paris).
        byTrain(saarbruecken,paris).
        byPlane(frankfurt,bangkok).
        byPlane(frankfurt,singapore).
        byPlane(paris,losAngeles).
        byPlane(bangkok,auckland).
        byPlane(losAngeles,auckland).


        travel(X, Y, go(X,Y,car)) :- byCar(X,Y).
        travel(X, Y, go(X,Y,plane)) :- byPlane(X,Y).
        travel(X, Y, go(X,Y,train)) :- byTrain(X,Y).

        travel(X,Y, go(X, Z, car, Route)) :- byCar(X,Z) , travel(Z,Y,Route).
        travel(X,Y, go(X, Z, plane, Route)) :- byPlane(X,Z) , travel(Z,Y,Route).
        travel(X,Y, go(X, Z, train, Route)) :- byTrain(X,Z) , travel(Z,Y,Route).
    """
    
    print(string)

def ex8():
    string = """
        Family facts
        family(person(tom, fox, date(7, may, 1950), works(bbc, 15200)),
            person(ann, fox, date(9, may, 1951), unemployed),
            [person(pal, fox, date(5, may, 1973), unemployed),
                person(jim, fox, date(5, may, 1973), unemployed)]).

        % Rule to find children born in a specific year
        child_born_in_year(Year, Name) :-
            family(_, _, Children),               
            member(person(Name, _, date(_, _, Year), _), Children). % Match children born in the given year
    """
    
    print(string)
