from sympy import *
from sympy.abc import i, n
import complexity_sort

def test_sort():

    # refactor to use indices.

    # Lists 1 to 3 taken and verified against
    #  MIT OCW 6.006 Fall 2011 Problem Set 1 Question 1.1
    l1 = [1.000001 ** n, n ** 0.99999999 * log(n), 10000000*n, n**2, sin(n) + 100000]
    l1_sorted = [l1[ind] for ind in (4, 1, 2, 3, 0)]
    assert complexity_sort.sort(l1) == l1_sorted

    l2 = [2**(1000000*n), binomial(n,2),n * sqrt(n)]
    l2_sorted = [l2[ind] for ind in (2, 1, 0)]
    assert complexity_sort.sort(l2) == l2_sorted

    l3 = [n ** sqrt(n), 2**n, n**10 * 2**(n/2), Sum(i+1, (i, 0, n))]
    l3_sorted = [l3[ind] for ind in (3, 0, 2, 1)]
    assert complexity_sort.sort(l3) == l3_sorted

    # List 4 taken and verified against MIT OCW 6.006 Fall 2011
    #   Quiz 1 Question 2
    l4 = [n**pi, pi**n, binomial(n, 5), sqrt(2**sqrt(n)), binomial(n, n-4),
          2**(log(n)**4), n**(5*(log(n))**2), n**4 * binomial(n, 4)]
    l4_sorted = [l4[ind] for ind in (0, 4, 2, 7, 6, 5, 3, 1)]
    assert complexity_sort.sort(l4) == l4_sorted

    # List 5 taken and verified against MIT OCW 6.046J Winter 2015
    #   Problem Set 1 Exercise 1.1
    l5 = [5*n, 4*log(n), 4*log(log(n)), n**4, n**(1/2)*(log(n))**4,
          (log(n))**(5*log(n)), n**log(n), 5**n, 4**(n**4), 4**(4**n),
          5**(5**n), 5**(5*n), n**(n**(1/5)), n**(n/4), (n/4)**(n/4)]
    l5_sorted = [l5[ind] for ind in (2, 1, 4, 0, 3, 5, 6, 12,
                                     7, 11, 14, 13, 8, 9, 10)]
    assert complexity_sort.sort(l5) == l5_sorted
