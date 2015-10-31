from itertools import combinations
import random
from operator import itemgetter


class Point:
    """ A Point Class """
    def __init__(self, components, clazz=None):
        """
        :param components: a sequence of size N containing the components of point, where N is the dimension of space.
        :param clazz: a type/class assigned to the point
        """
        self.components = components
        self.clazz = clazz
  
    def norm(self, metric):
        """
        :param metric: a function that returns the distance of the point from the origin
        :return: the norm of the point as defined by metric
        """
        return metric(self.components)

    def normalize(self, metric):
        """
        :param metric:  a function that returns the distance of the point from the origin
        :return: normalizes the point to norm 1 as defined by the metric function and returns self with new components
        """
        n = self.norm(metric)
        self.components = [v/n for v in self.components]
        return self

    def distance_to(self, other_point, metric):
        """
        :param other_point: other point object to measure distance to
        :param metric: a function that returns the distance of the point from the origin
        :return: distance from self to other point as defined by metric function
        """
        d = [self.components[i] - other_point[i] for i in range(len(other_point))]
        return metric(d)

    def distances(self, points, metric):
        """
        :param points: an iterable containing all the points to measure distances to
        :param metric: a function that returns the distance of the point from the origin
        :return: a list containing distance of self to all other points (excluding itself)
        """
        distances = [self.distance_to(point, metric) for point in points if self is not point]
        return distances

    def nearest_point(self, points, metric):
        """
        :param points: iterable sequence of points
        :param metric: a function that returns the distance of the point from the origin
        :return: the point in points nearest to self
        """
        distances = self.distances(points, metric)
        nearest_point_index = min(enumerate(distances), key=itemgetter(1))[0]
        return points[nearest_point_index]

    def perturb(self, distribution):
        """
        :param distribution: a random number generator function
        :return: alters each self's components using the distribution function and returns self
        """
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
    """ A container class for point objects """
    def __init__(self, points):
        self.points = points

    def combinations(self, n):
        """
        :param n: an integer value
        :return: an iterable of every combination of n points
        """
        return combinations(self.points, n)

    def distances(self, metric):
        """
        :param metric: a function that returns the distance of the point from the origin
        :return: an iterable of distances between every possible point pair in the point cloud
        """
        two_point_combos = self.combinations(2)
        return (p1.distance_to(p2, metric) for (p1, p2) in two_point_combos)

    def normalize(self, metric):
        """
        :param metric: a function that returns the distance of the point from the origin
        :return: calls normalize on every point in the point cloud and returns self when done
        """
        self.points = [point.normalize(metric) for point in self.points]
        return self

    def perturb_points(self, distribution):
        """
        :param distribution: a random numnber generator function
        :return: calls perturb on every point in the point cloud and returns self when done
        """
        return [point.perturb(distribution) for point in self.points]

    @classmethod
    def generate(cls, N, K, distribution):
        """
        A factory method that generates a point cloud on given paramters
        :param N: dimensionality of space
        :param K: number of points
        :param distribution: a random number generator function that generates components for the points
        :return: a point cloud object with K points of N dimension
        """
        points = [Point([distribution() for i in range(N)]) for j in range(K)]
        return PointCloud(points)

    @classmethod
    def generate_with_classes(cls, N, K, distribution, classes):
        """
        A factory method that generates a point cloud on given paramters
        :param N: dimensionality of space
        :param K: number of points
        :param distribution: a random number generator function that generates components for the points
        :return: a point cloud object with K points of N dimension
        :param classes: a container of classes that will be randomly assigned to each point
        :return: a point cloud object with K points of N dimension, each of which has been randomly assigned a class
        """
        points = [Point([distribution() for i in range(N)], random.choice(classes)) for j in range(K)]
        return PointCloud(points)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        return self.points[item]





        








