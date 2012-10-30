import itertools
import operator
import random

from math import sqrt

from ..lsh import MinHashSignature, jaccard_sim

################################################################################
#  Testing utilities
################################################################################
def randset():
    """Return a random set.  These values of n and k have wide-ranging
    similarities between pairs.
    """
    n = random.choice(range(5, 20))
    k = 10
    return set( random.choice(range(k)) for _ in range(n) )

def sigsim(X, Y, dim):
    """Return the similarity of the two signatures"""
    return sum(map(operator.eq, X, Y)) / float(dim)


################################################################################
# Le tests
################################################################################
def test_signature_length():
    """Signatures should have correct dimension"""
    dim = 100
    mh = MinHashSignature(dim)
    assert dim == len(mh.sign(randset()))

def test_consistent_signature():
    """Signatures should be consistent"""
    mh = MinHashSignature(100)
    s = randset()
    assert mh.sign(s) == mh.sign(s)

def test_signature_similarity():
    """The probability that two sets' signatures match at some index
    are equal is equal to the Jaccard similarity between the two"""
    dim = 100
    n_tests = 100
    expected_error = 1 / sqrt(dim) # Expected error is O(1/sqrt(dim))
    mh = MinHashSignature(dim)
    err = 0.0

    for test in range(n_tests):
        # Create random sets and their signatures
        sets = (randset(), randset())
        sigs = map(mh.sign, sets)

        # Calculate true jaccard similarity, and sim of signatures
        jsim = jaccard_sim(*sets)
        ssim = sigsim(*sigs, dim=dim)

        # Accumulate error
        err += abs(jsim - ssim)

    # Over n_tests large, we should be within upper bound of expected error.
    avg_err = err / n_tests
    assert expected_error >= avg_err, "Accuracy test failed. (avg error: %f)" % avg_err
