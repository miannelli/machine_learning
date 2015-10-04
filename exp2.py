import random

N_Values = [2]  # The dimensionality of space
K_Values = [100]  # The number of point values
L_Values = [2]

def norm(point, l=2):
    """ Given a point, returns the l-norm """
    return (sum([v**l for v in point]))**(1/l)

def normalize(point, l=2):
    """ Given a point, scales it to l-norm one"""
    n = norm(point, l)
    return [v/n for v in point]


def distance(point1, point2, l=2):
    """ Given two points and an L, returns the l-distance between the two points. """
    d = [point1[i] - point2[i] for i in range(len(point1))]
    return norm(d, l)

def distances(points, l=2):
    """ Given a list of points, return a list of all possible distances between two points"""
    distances = []
    while points:
        baseline = points.pop()
        distances.extend([distance(baseline, point, l) for point in points])
    return distances

class Result:
    def __init__(self, N, K, L, dmin, dmax):
        self.N = N
        self.K = K
        self.L = L
        self.dmin = dmin
        self.dmax = dmax
        self.r = dmin

    def __repr__(self):
        return "<N: {N}, K: {K}, L: {L}, r: {r}>".format(N=self.N, K=self.K, L=self.L, r=self.r)

def run():
    """ Runs the experiment """
    results = []
    for K in K_Values:
        for N in N_Values:
            for L in L_Values:
                points = [normalize([random.gauss(0, 1) for i in range(N)], L) for j in range(K)]
                d = distances(points)
                dmin = min(d)
                dmax = max(d)
                r = (dmin/dmax)
                results.append(Result(N, K, L, dmin, dmax))
    return results


