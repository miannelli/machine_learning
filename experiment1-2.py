import point
from helpertools import Metric, Xi
import random
import tablemaker
from copy import deepcopy
from confusionmatrix import ConfusionMatrix

trials = 10
N_Values = list(range(1, 11)) + list(range(20, 101, 10))  # The dimension of space
K_Values = [k for k in range(10, 301, 10)]  # The number of point values
metrics = [Metric(ord) for ord in [2]]  # Different norms to use
distribution = (lambda: random.uniform(0, 1))  # Point Distribution
xis = [Xi((lambda: random.gauss(0, sigma)), sigma) for sigma in [.05, .1, .15, .2, .25]]
M = 100


def trial(trial_number, metric, K, N, distribution, xi):
    X = point.PointCloud.generate_with_classes(N, K, distribution, [True, False])
    Y = point.PointCloud.generate(N, M, distribution)
    for y in Y:
        closest_point = y.nearest_point(X, metric)
        y.clazz = closest_point.clazz
    perturbed_Y = deepcopy(Y).perturb_points(xi)
    for y in perturbed_Y:
        closest_point = y.nearest_point(X, metric)
        y.clazz = closest_point.clazz
    confusion_matrix = ConfusionMatrix.generate_from_point_clouds(Y, perturbed_Y)
    result = [trial_number, metric, K, N, xi.sigma] + confusion_matrix.row()
    print(result)
    return result


results = [trial(trial_number, metric, K, N, distribution, xi) for metric in metrics for N in N_Values for K in K_Values
           for xi in xis for trial_number in range(0, trials)]
tablemaker.make_table('experiment1-2', ['Trial', 'Metric', 'K', 'N', 'sigma'] + ConfusionMatrix.headers(), results)




