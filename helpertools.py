from numpy.linalg import norm


class Metric:
    """
    A metric class used to contain the metric function to be used and a label (for graphing purposes).
    """
    def __init__(self, ord):
        self.norm = lambda vector: norm(vector, ord)
        self.ord = ord

    def __call__(self, vector):
        return self.norm(vector)

    def __repr__(self):
        return str(self.ord)

    def __str__(self):
        return str(self.ord)


class Xi:
    """
    A Xi class used to contain the distribution function to be used and a label (for graphing purposes).
    """
    def __init__(self, distribution, sigma):
        self.distribution = distribution
        self.sigma = sigma

    def __call__(self):
        return self.distribution()

    def __repr__(self):
        return str(self.sigma)

    def __str__(self):
        return str(self.sigma)