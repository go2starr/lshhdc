## LSHHDC : Locality-Sensitive Hashing based High Dimensional  Clustering  

## Locality-sensitive hashing  
Unlike cryptographic hashing where the goal is to map objects to
numbers with a low collision rate and high randomness, the goal of LSH
is to map similar elements to similar keys with high probability.

An obvious use of this technique is clustering.  From Rajamaran,
"Mining of Massive Datasets":

> A family F of functions is said to be (d1, d2, p1, p2)-sensitive if
> for every f in F:  
> 1. If d(x,y) ≤ d1, then the probability that f(x) = f(y) is at least p1.  
> 2. If d(x,y) ≥ d2, then the probability that f(x) = f(y) is at most p2.  



