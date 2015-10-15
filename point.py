import numpy as np

class Point:

    def __init__(self, components):
        self.components = components

    def calculate_distance(self, other_points, metric):
        op_list = other_points.tolist()
        curr_min = float("inf")
        curr_max = 0
        for op in op_list:
            dist = metric(self, op)
            if curr_min > dist:
                curr_min=dist
            if curr_max < dist:
                curr_max=dist
        return curr_min,curr_max

    @classmethod
    def generate(cls, number, dimension, distribution):
        points = np.empty([number, dimension])
        for i in range(0, number):
            for j in range(0, dimension):
                points[i][j] = distribution
        return points
