from lsh import Cluster, jaccard_sim

from .utils import *


def test_same_set():
    """A set should be clustered with itself"""
    s = randset()
    cluster = Cluster()
    cluster.add_set(s)
    cluster.add_set(s)
    assert len(cluster.get_sets()) == 1

def test_similar_sets():
    """Two similar sets should be clustered"""
    cluster = Cluster()
    cluster.add_set("abcdefg")
    cluster.add_set("abcdefghi")
    assert len(cluster.get_sets()) == 1

def test_dissimilar_sets():
    """Two non-similar sets should not be clustered"""
    cluster = Cluster()
    cluster.add_set("12345abcdef")
    cluster.add_set("1234567890z")
    print cluster.get_sets()
    assert len(cluster.get_sets()) == 2

def test_cluster_threshold():
    """Expected error for threshold to similarity should be reasonable"""
    n_tests = 50
    dim = 15
    expected_error = 0.20

    tot_err = 0
    for test in range(n_tests):
        # Get some sets and their similarities
        sets = (randset(), randset())
        jsim = jaccard_sim(*sets)

        # Find the threshold at which they cluster together
        for threshold in range(1, 100, 5):
            threshold = float(threshold) / 100
            cluster = Cluster(dim, threshold)
            cluster.add_set(sets[0])
            cluster.add_set(sets[1])
            if len(cluster.get_sets()) == 2:
                tot_err += abs(jsim - threshold)
                break
    avg_err = float(tot_err) / n_tests
    assert avg_err <= expected_error
