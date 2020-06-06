from statistics import NormalDist

def Q(q):

    return 1 - NormalDist(mu=0, sigma=1).cdf(q)
