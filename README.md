# complexity_sort

 __Sorts functions by their asymptotic complexity in increasing order__

![](http://i.imgur.com/3tPGLZB.png)

```python
>>> import complexity_sort
>>> sample_funcs = ['1.000001 ** n',
...                 'n**0.9999999 * log(n)',
...                 '1000000 * n',
...                 'n**2',
...                 'sin(n) + 10000000']
>>> complexity_sort.sort(sample_funcs, parser='sympy')
[sin(n) + 10000000, n**0.9999999*log(n), 1000000*n, n**2, 1.000001**n]
```

![](http://i.imgur.com/r0SZF0N.png)



## Dependencies

- [SymPy 1.0](https://github.com/sympy/sympy/releases/tag/sympy-1.0), although it may work on versions as early as 0.7.7 (_untested_)

## Usage

The interface of __complexity_sort__ comprises of a single function, `sort()`.  

```
>>> help(complexity_sort.sort)
Help on function sort in module complexity_sort.complexity_sort:

sort(it, variable=None, parser=None)
    Sort an iterable of functions by their asymptotic complexity.
    
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

```

The important thing to note here is that all functions must have ranges restricted to the positive reals in order to be admissible. This does include oscillating functions. 

Furthermore, __complexity_sort__ is __not guaranteed__ to produce a sorted list for all admissible functions. It __is guaranteed__ to produce a _correct_ sorted list should it prove capable of returning a sorted list however, or at least that is the idea.

## Implementation details

### Background

__complexity_sort__ is nothing more than the application of a few ideas, leaning heavily on the symbolic mathematics library SymPy. 

<a name=lemma1></a>
- __Lemma 1__

	 ![](http://i.imgur.com/6ixIDwT.png)

<a name=lemma2></a>

- __Lemma 2__
	 ![](http://i.imgur.com/aFRenjL.png)

- __The transitive relational properties of Θ, Ω, ω, _O_, _o___

### How it works

#### Direct approach first

We first try to sort the iterable simply using Python's built-in [Timsort algorithm](https://en.wikipedia.org/wiki/Timsort)<sup>1</sup> by applying a custom comparator between functions. 

This custom comparator: 

1. Tries to directly apply [Lemma 1](#lemma1) to determine the relation between two functions. 
2. If the limit for Lemma 1 does not exist (often because the function is oscillating), the comparator tries to apply [Lemma 2](#lemma2) to determine the relation. 


#### Falling back to topological sort
Should both attempts between two functions fail with the custom comparator, we reconsider our sorting with a [directed graph](https://en.wikipedia.org/wiki/Directed_graph)<sup>2</sup>. 

We let each function denote a vertex in our graph, and let the directed edges represent a "greater-than" relation between two functions. 

We then attempt to apply a topological sort to the graph with the hope that it contains no [directed cycles](https://en.wikipedia.org/wiki/Cycle_graph#Directed_cycle_graph)<sup>3</sup>. This is permissible due to the transitive relational properties of the asymptotic definitions. 

##### Example

Consider the list of functions from above:

![](http://i.imgur.com/3tPGLZB.png)

We cannot easily determine the relation between `1.000001^n` and `10000000n` with Lemma 1 and Lemma 2. However as long as they are separable in asymptotic complexity order by at least one other function we can still we can sort the list. 

More formally, we require that our corresponding graph is a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph)<sup>4</sup>. Our corresponding directed graph in this case looks something like this. 

![](http://i.imgur.com/tLsQ53b.png)

This graph is evidently acyclic, as `10000000n` is linear, `n^2` is quadratic, and `1.000001^n` is exponential => `n^2` ensures there is no cycle between the incomparable elements. Correspondingly, `complexity_sort.sort` can successfully sort the functions.  

#### Failure

Should both lemmas fail with direct sorting and our directed graph contain a cycle, `complexity_sort.sort` will indicate that it does not have enough comparable elements to sort the iterable. 

```python
>>> a = ['1.000001 ** n',
...         'n**0.99999999 * log(n)',
...         '10000000*n', 
...         'sin(n) + 100000'] # remove the quadratic n^2
>>> complexity_sort.sort(a, parser='sympy') 
ValueError: List is not sortable with number of comparable elements.
```

## To be implemented

- More test cases on a greater diversity of function lists.

- Provide proofs for these lemmas using basic limit definitions. 

If you see anything else that could be improved, by all means go for it or drop me a mail and let me know your thoughts. My email can be find on my [about me page](https://mitchelledwardsnaith.github.io/about/)

## Licence 

To put here

---

#### References

- 1 : Timsort (Wiki): https://en.wikipedia.org/wiki/Timsort
- 2 : Directed graph (Wiki) : https://en.wikipedia.org/wiki/Directed_graph
- 3 : Directed cycles (Wiki) : https://en.wikipedia.org/wiki/Cycle_graph#Directed_cycle_graph
- 4 : Directed acyclic graph (Wiki) : https://en.wikipedia.org/wiki/Directed_acyclic_graph















 

