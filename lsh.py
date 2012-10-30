"""
lsh.py

Algorithms based on 'Mining of Massive Datasets'
"""
from unionfind import UnionFind


class Signature:
    """Signature Base class."""

    def __init__(self, dim):
        self.dim = dim
        self.hashes = self.hash_functions()

    def hash_functions(self):
        """Returns dim different hash functions"""
        pass

    def sign(self, object):
        """Return the signature for object s"""
        pass


class MinHashSignature(Signature):
    """Creates signatures for sets/tuples using minhash."""

    def hash_functions(self):
        """Return dim different hash functions"""
        def hash_factory(n):
            return lambda x: hash(str(n) + str(x) + "salt")
        return [ hash_factory(_) for _ in range(self.dim) ]
    
    def sign(self, s):
        """Returns minhash signature for set s"""
        sig = [ float("inf") ] * self.dim
        for hash_ix, hash_fn in enumerate(self.hashes):
            sig[hash_ix] = min(hash_fn(value) for value in s)
        return sig        


class LSH:
    """Locality sensitive hashing.  Uses a banding approach to hash
    similar signatures to the same buckets."""
    def __init__(self, length, threshold):
        self.length = length
        self.threshold = threshold
        self.bandwidth = self.get_bandwidth(length, threshold)

    def hash(self, sig):
        """Generate hashvals for this signature"""
        for band in zip(*(iter(sig),) * self.bandwidth):
            yield hash("salt" + str(band) + "tlas")
        
    def get_bandwidth(self, n, t):
        """Approximates the bandwidth (number of rows in each band)
        needed to get threshold.  
        
        Threshold t = (1/b) ** (1/r) where
        b = #bands
        r = #rows per band
        n = b * r = #elements in signature
        """
        
        best = n, 1
        minerr  = float("inf")
        for r in range(1, n + 1):
            try:
                b = 1. / (t ** r)
            except:             # Divide by zero, your signature is huge
                return best
            err = abs(n - b * r)
            if err < minerr:
                best = r
                minerr = err
        return best

    def get_threshold(self):
        r = self.bandwidth
        b = self.length / r
        return (1. / b) ** (1. / r)


class Cluster:
    """Clusters sets with Jaccard similarity above threshold with high
    probability.

    Algorithm based on Rajaraman, "Mining of Massive Datasets":
    1. Generate set signature
    2. Use LSH to map similar signatures to same buckets
    3. Use UnionFind to merge buckets containing same values
    """
    def __init__(self, width=10, threshold=0.5):
        self.width = width
        self.unionfind = UnionFind()
        self.signer = Signature(width)
        self.hasher = LSH(width, threshold)
        self.hashmap = {}

    def add_set(self, s, label=None):
        # A label for this set
        if not label:
            label = s

        # Add to unionfind structure
        self.unionfind[label]

        # Get signature
        sig = self.signer.sign(s)

        # Union labels with same LSH keys
        for hshval in self.hasher.hash(sig):
            self.hashmap.setdefault(hshval, []).append(label)
            self.unionfind.union(label, self.hashmap[hshval][0])

    def get_sets(self):
        return self.unionfind.sets()

    
def shingle(s, k):
    """Generate k-length shingles of string s"""
    k = min(len(s), k)
    for i in range(len(s) - k + 1):
        yield s[i:i+k]

def hshingle(s, k):
    """Generate k-length shingles of s into m buckets"""
    for s in shingle(s, k):
        yield hash(s)

def jaccard_sim(X, Y):
    x = set(X)
    y = set(Y)
    return float(len(x & y)) / len(x | y)

def jaccard_dist(X, Y):
    return 1 - jaccard_sim(X, Y)

# myset = [
#     (1,2,3,4,6),                  # 
#     (1,2,3,4,5)                 # 4 / 6 = 75
#     ]

# N = 100
# K = 1
# T = 0.70

# clusterer = Cluster(N, T)

# print "True threshold: %f" % clusterer.hasher.get_threshold()
# print clusterer.hasher.bandwidth

# for s in myset:
#     clusterer.add_set(s, "".join(str(_) for _ in s))

# for s in clusterer.get_sets():
#     print s

# if __name__ == "__main__":
#     # Run some tests :)
#     N = 1000
#     thresholds = [ 0.25, 0.50 ] 
#     trials = 10
#     setwidth = 10
#     setmax = 100
    
#     import random
    
#     def randset(setmax, setwidth):
#         return tuple( random.choice(range(setmax)) for _ in range(setwidth) )
    
#     for n in range(1, 100, 10):
#         err = 0
#         for trial in range(trials):
#             x = randset(setmax, setwidth)
#             y = randset(setmax, setwidth)
#             sim = jaccard_sim(x, y)
            
#             for threshold in range(1, 100):
#                 threshold = float(threshold) / 100
#                 clusterer = ClusterFuck(n, threshold)
#                 clusterer.add_set(x)
#                 clusterer.add_set(y)
#                 if len(clusterer.get_sets()) == 2:
#                     err += abs(sim - threshold)
#                     break
#         print "%d: %f" % (n, 100 * err / trials)
