from itertools import combinations
import random
from operator import itemgetter


class Point:
    """ A Point Class """
    def __init__(self, components, clazz=None):
        self.components = components
        self.clazz = clazz
  
    def norm(self, metric):
        return metric(self.components)

    def normalize(self, metric):
        n = self.norm(metric)
        self.components = [v/n for v in self.components]
        return self

    def distance_to(self, other_point, metric):
        d = [self.components[i] - other_point[i] for i in range(len(other_point))]
        return metric(d)

    def distances(self, points, metric):
        distances = [self.distance_to(point, metric) for point in points if self is not point]
        return distances

    def nearest_point(self, points, metric):
        distances = self.distances(points, metric)
        nearest_point_index = min(enumerate(distances), key=itemgetter(1))[0]
        return points[nearest_point_index]

    def perturb(self, distribution):
        xi = distribution()
        self.components = [component + xi for component in self.components]
        return self

    def __len__(self):
        return len(self.components)

    def __getitem__(self, item):
        return self.components[item]

    def __repr__(self):
        return "<{comps} - class: {cl}>".format(comps=str(self.components), cl=self.clazz)


class PointCloud:
    def __init__(self, points):
        self.points = points

    def combinations(self, number):
        return combinations(self.points, number)

    def distances(self, metric):
        two_point_combos = self.combinations(2)
        return (p1.distance_to(p2, metric) for (p1, p2) in two_point_combos)

    def normalize(self, metric):
        self.points = [point.normalize(metric) for point in self.points]
        return self

    def perturb_points(self, distribution):
        return [point.perturb(distribution) for point in self.points]

    @classmethod
    def generate(cls, N, K, distribution):
        points = [Point([distribution() for i in range(N)]) for j in range(K)]
        return PointCloud(points)

    @classmethod
    def generate_with_classes(cls, N, K, distribution, classes):
        points = [Point([distribution() for i in range(N)], random.choice(classes)) for j in range(K)]
        return PointCloud(points)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        return self.points[item]





        








