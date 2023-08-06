from itertools import chain, combinations


def powerset(iterable, min_size=0):
    "powerset([1,2,3], 0) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable((combinations(s, r)) for r in range(min_size, len(s) + 1))


def cartesian_product():
    return list(itertools.chain(*(itertools.combinations(Rs, i) for i in range(2, k))))