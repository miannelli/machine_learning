import point
from helpertools import Metric
import random
from numpy import inf
from statistics import mean, stdev
import tablemaker


def trial(trial_number, metric, K, N, distribution):
    point_cloud = point.PointCloud.generate(N, K, distribution)
    point_distances = (point.distances(point_cloud.points, metric) for point in point_cloud.points)
    ratios = [min(distances)/max(distances) for distances in point_distances]
    result = trial_number, metric, K, N, mean(ratios), stdev(ratios)
    print(result)
    return result

N_Values = list(range(1, 11)) + list(range(20, 101, 10))  # The dimension of space
K_Values = [5, 50, 500]  # The number of point values
metrics = [Metric(ord) for ord in [1, 2, inf]]  # Different norms to use
trials = 25

distribution = (lambda: random.uniform(0, 1))  # Point Distribution

results = [trial(trial_number, metric, K, N, distribution) for metric in metrics for N in N_Values for K in K_Values for trial_number in range(trials)]
tablemaker.make_table('experiment1-1', ['TrialNumber', 'Metric', 'K', 'N', 'Mean', 'StandardDeviation'], results)