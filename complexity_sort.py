#!/usr/bin/env python

import functools
import itertools
import operator
import numbers
import sympy.parsing.sympy_parser
import sympy.parsing.mathematica
import sympy.utilities.iterables
from sympy.series.limitseq import limit_seq, S
from sympy.calculus.util import AccumulationBounds

__author__ = 'Mitchell Snaith'
__date__ = '2016-08-01'

_parse_d = {'mathematica': sympy.parsing.mathematica.parse, 'sympy': sympy.parsing.sympy_parser.parse_expr}


def sort(it, variable=None, parser=None):
    """
    Sort iterable of functions l by their asymptotic complexity.

    Admissible functions:
        - Must have ranges restricted to the non-negative real numbers.

    Parameters:
        it (str or sympy.Expr) :
            Iterable of functions to be sorted

        variable (str or sympy.Expr, optional):
            Variable to compare complexities with respect to.
            Only necessary if there are multiple variables in the functions.
            Defaults to None.

        parser (str, optional):
            Parser with which to parse functions if iterable is of string type.
            Options are 'sympy' and 'mathematica'.
            Defaults to None.

    Returns:
         list : A sorted list of functions upon success.

    Raises:
        ValueError:
            - If the iterable does not contain enough comparable elements to sort.
    """
    if parser:
        use_parser = _parse_d[parser]
        it = [use_parser(item, evaluate=False) for item in it]
        if variable is not None:
            variable = use_parser(variable)

    if not variable:   # we must determine the lone variable to calculate with respect to
        free_syms = functools.reduce(operator.or_, [expr.free_symbols for expr in it])
        if len(free_syms) == 1:
            variable = free_syms.pop()
        elif free_syms == 0:
            return it
        else:
            raise ValueError('There are multiple variables within '
                             'the iterable of expressions.\n '
                             'Please specify a variable to order the complexities with respect to.')

    compare_with_var = functools.partial(_order_comp, variable=variable)
    try:
        return sorted(it, key=functools.cmp_to_key(compare_with_var))
    except _ComparisonException:   # we cannot apply direct sort -> produce a directed graph
        return _dag(it, variable)


class _ComparisonException(Exception):
    pass


def _dag(l, variable):

    vertices = l
    edges = list()

    for i, j in itertools.combinations(l, 2):
        try:
            order = _order_comp(i, j, variable)
        except _ComparisonException:
            order = None 
        if order:
            edges.append((i, j)[::-order])
    try:
        return sympy.utilities.iterables.topological_sort((vertices, edges))
    except (ValueError, TypeError):
        raise ValueError('Iterable is not sortable with number of comparable elements.')


@functools.lru_cache()
def _order_comp(a, b, variable=None):
    a_const = not a.has(variable)
    b_const = not b.has(variable)
    if a_const and b_const:
        return 0
    elif a_const:
        return -1
    elif b_const:
        return 1

    orig_quot = (a / b).combsimp()
    lim = limit_seq(orig_quot, variable)
    if lim is S.Zero:
        return -1
    elif lim in (S.Infinity, -S.Infinity):
        return 1
    elif lim is numbers.Number and lim > 0:
        return 0
    else:
        return _use_sup_inf_limits(a, b, variable)


def _use_sup_inf_limits(a, b, sym):
    limits_a, limits_b = limit_seq(a, sym), limit_seq(b, sym)
    if any(i is None for i in (limits_a, limits_b)):
        none_val = a if limits_a is None else b
        raise ValueError(str.format('The term {0} cannot be handled.', none_val))

    sup_a, inf_a = _max_and_min(limits_a)
    sup_b, inf_b = _max_and_min(limits_b)

    sup_q = limit_seq(sup_a/sup_b, sym)
    inf_q = limit_seq(inf_a/inf_b, sym)

    if sup_q is S.Zero:
        return -1
    elif inf_q is S.Infinity:
        return 1
    elif sup_q is S.NaN or inf_q is S.NaN:
        raise _ComparisonException
    elif sup_q > 0 and inf_q > 0:
        return 0

    raise _ComparisonException


def _max_and_min(lim):
    if type(lim) is AccumulationBounds:   # indicates we have an infinite bound 
        return lim.max, lim.min
    return lim, lim







