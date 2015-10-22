from numpy.linalg import norm


class RollingAverage:

    def __init__(self):
        self.average = 0.0
        self.count = 0

    def __iadd__(self, value):
        self.average = ((self.average*self.count + value)/(self.count + 1))
        self.count += 1
        return self

    def __call__(self):
        if self.count:
            return self.average
        else:
            raise ArithmeticError('Average undefined for empty empty array')

    def __repr__(self):
        return str(self.average)


class Metric:

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
    def __init__(self, distribution, sigma):
        self.distribution = distribution
        self.sigma = sigma

    def __call__(self):
        return self.distribution()

    def __repr__(self):
        return str(self.sigma)

    def __str__(self):
        return str(self.sigma)