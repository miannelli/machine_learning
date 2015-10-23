import point
from helpertools import Metric, Xi
import random
import tablemaker
from copy import deepcopy
from confusionmatrix import ConfusionMatrix


N_Range = 300
K_Range = 200
metrics = [Metric(2)]
sigma_range = 1.0
distributions = [(lambda: random.uniform(0, 1))]
trials = 2000
M = 100


def generate_params(n_range, k_range, metrics, distributions, sigma_range):
    N = random.randint(1, n_range)
    K = random.randint(1, k_range)
    distribution = random.choice(distributions)
    sigma = random.uniform(0, sigma_range)
    xi = Xi((lambda: random.gauss(0, sigma)), sigma)
    metric = random.choice(metrics)
    return N, K, distribution, xi, metric


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

results = []
for trial_number in range(trials):
    N, K, distribution, xi, metric = generate_params(N_Range, K_Range, metrics, distributions, sigma_range)
    results.append(trial(trial_number, metric, K, N, distribution, xi))


tablemaker.make_table('experiment1-2(1)', ['Trial', 'Metric', 'K', 'N', 'sigma'] + ConfusionMatrix.headers(), results)




