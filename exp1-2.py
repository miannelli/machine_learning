#!/opt/local/bin/python3.4

'''
Jonathan Gryak
Machine Learning, Fall 2015
Exercise 1-2
'''

#import packages

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import spatial
import argparse,sys
import random,copy

#dimension of the space
n=10
#the number of points in the training set
k=10
#the number of points in the data set
m=10
#std deviation
sigma = .1
#classes
class_list=['c1','c2']

#process command line arguments
parser = argparse.ArgumentParser(description="ML Experiment 1_2")
parser.add_argument('-n',metavar='<n>', help="n - The dimension")
parser.add_argument('-k',metavar='<k>', help="k - The number of samples")
#parse arguments
args =	parser.parse_args()

if(args.n):
	try:
		n=int(args.n)
	except (ValueError) as e:
		print(args.n,": Not an integer",file=sys.stderr)
		sys.exit(-1)
if(args.k):
	try:
		k=int(args.k)
	except (ValueError) as e:
		print(args.k,": Not an integer",file=sys.stderr)
		sys.exit(-1)

#point class, represents a point of dimension dim, with an optional class _class
class Point:
	def __init__(self,dim,dist=None,dist_args=None,_class=None):
		"""set the dimension of the point"""
		self.dim = dim
		"""initialize point array either to 0 or from a specified distribution"""
		if dist is None:
			self.point=[0 for x in range(dim)]
		else:
			self.point=[dist(*dist_args) for x in range(dim)]
		"""set the assigned class"""
		self._class=_class
	def __repr__(self):
		return "<{D}-values,class>: <{P}, {C}>".format(D=self.dim, P=str(self.point).strip('[]'), C=self._class)
	
#generate num_points points (vectors) of length dim with values provided by function dist
def generatePoints(num_points,dim,dist,dist_args,classes=None):
	#create array of num_points of dimension dim.
	points = []
	for i in range(0,num_points):
		#create new point
		new_point=Point(dim,dist,dist_args)
		#if classes were defined
		if classes is not None:
			new_point._class=random.choice(classes)
		points.append(new_point)
	return points

#calculate min and max distance from point to other_points, using distance function
def norm(point, l=2):
    """ Given a point, returns the l-norm """
    #test if l is infinite:
    if l == float('inf'):
    	return max(point)
    else:
    	return (sum([v**l for v in point]))**(1/l)

def distance(point1, point2, l=2):
    """ Given two points and an L, returns the l-distance between the two points. """
    d = [point1.point[i] - point2.point[i] for i in range(len(point1.point))]
    return norm(d, l)
	
def distances(points, l=2):
    """ Given a list of points, return a list of all possible distances between two points"""
    distances = []
    while points:
        baseline = points.pop()
        distances.extend([distance(baseline, point, l) for point in points])
    return distances

#returns the point in the list other_points which is closest to point
def closest_point(point, other_points, l=2):
	distances = [distance(point,p,l) for p in other_points]
	return other_points[np.argmin(distances)]	

#perturbs a list of points by adding a sample from the distribution dist (with dist_args) to each component of the point
def perturb_points(points,dist,dist_args):
	#sample the distribution
	xi = dist(*dist_args)
	#create copy of points
	perturbed_points = copy.deepcopy(points)
	for p in perturbed_points:
		p.point = [x + xi for x in p.point]
	return perturbed_points

#run experiment 1_2 with the passed parameters, returning the confusion matrix
def run_experiment1_2(n,k,m,sigma,class_list):
	#generate training data
	training_data=generatePoints(k,n,np.random.uniform,[0,1],class_list)
	#generate data set
	data_set=generatePoints(m,n,np.random.uniform,[0,1])
	#perturb data_set 
	perturbed_data_set = perturb_points(data_set,np.random.normal,[0,sigma])

	data_set_size = len(data_set)
	num_classes = len(class_list)
	#classify points
	for i in range(data_set_size):
		#assign y to the class of its closest point
		data_set[i]._class = closest_point(data_set[i],training_data)._class
		#assign y tilde to the class of its closest point
		perturbed_data_set[i]._class = closest_point(perturbed_data_set[i],training_data)._class

	#calculate confusion matrix
	conf_matrix = [ [0 for i in range(num_classes)] for j in range(num_classes)]

	true_classes = [x._class for x in data_set]
	assigned_classes = [x._class for x in perturbed_data_set]

	#for each classification
	for i in range(num_classes):	
		for j in range(num_classes):
			conf_matrix[i][j] = sum(1 if a==class_list[i] and b ==class_list[j] else 0 for a,b in zip(true_classes,assigned_classes))/data_set_size
	return conf_matrix

#run experiment 1_2 over a range of data
n_vals = list(range(10,110,10))
k_vals = list(range(10,110,10))
s_vals = np.arange(.1,1.1,.1)
num_classes=len(class_list)


#arrays for plotting
true_positives = []
false_positives = []
false_negatives = []
true_negatives = []

#vary dimension
for i in range(len(n_vals)):
	cm = run_experiment1_2(n_vals[i],k,k,sigma,class_list);
	#flatten matrix
	flat_cm = [item for sublist in cm for item in sublist]
	true_positives.append(flat_cm[0])
	false_positives.append(flat_cm[1])
	false_negatives.append(flat_cm[2])
	true_negatives.append(flat_cm[3])

#Figure 1, four subplots
plt.figure(1,figsize=(11,8.5))

plt.subplot(411)
plt.title("Varying N, K={K}, Sigma={S}".format(K=k,S=sigma))
plt.xlabel("Dimension")
plt.ylabel("True Positives")
plt.plot(n_vals,true_positives,'b')

plt.subplot(412)
plt.xlabel("Dimension")
plt.ylabel("False Positives")
plt.plot(n_vals,false_positives,'r')

plt.subplot(413)
plt.xlabel("Dimension")
plt.ylabel("False Negatives")
plt.plot(n_vals,false_negatives,'m')

plt.subplot(414)
plt.xlabel("Dimension")
plt.ylabel("True Negatives")
plt.plot(n_vals,true_negatives,'g')

#arrays for plotting
true_positives = []
false_positives = []
false_negatives = []
true_negatives = []

#vary sample size
for j in range(len(k_vals)):
	cm = run_experiment1_2(n,k_vals[i],k_vals[i],sigma,class_list);
	#flatten matrix
	flat_cm = [item for sublist in cm for item in sublist]
	true_positives.append(flat_cm[0])
	false_positives.append(flat_cm[1])
	false_negatives.append(flat_cm[2])
	true_negatives.append(flat_cm[3])

#Figure 2, four subplots
plt.figure(2,figsize=(11,8.5))

plt.subplot(411)
plt.title("Varying K, N={N}, Sigma={S}".format(N=n,S=sigma))
plt.xlabel("Samples")
plt.ylabel("True Positives")
plt.plot(k_vals,true_positives,'b')

plt.subplot(412)
plt.xlabel("Samples")
plt.ylabel("False Positives")
plt.plot(k_vals,false_positives,'r')

plt.subplot(413)
plt.xlabel("Samples")
plt.ylabel("False Negatives")
plt.plot(k_vals,false_negatives,'m')

plt.subplot(414)
plt.xlabel("Samples")
plt.ylabel("True Negatives")
plt.plot(k_vals,true_negatives,'g')

#arrays for plotting
true_positives = []
false_positives = []
false_negatives = []
true_negatives = []

#vary std deviation
for s in range(len(s_vals)):
	cm = run_experiment1_2(n,k,k,s_vals[s],class_list);
	#flatten matrix
	flat_cm = [item for sublist in cm for item in sublist]
	true_positives.append(flat_cm[0])
	false_positives.append(flat_cm[1])
	false_negatives.append(flat_cm[2])
	true_negatives.append(flat_cm[3])

#Figure 3, four subplots
plt.figure(3,figsize=(11,8.5))

plt.subplot(411)
plt.title("Varying Sigma, N={N}, K={K}".format(N=n,K=k))
plt.xlabel("Sigma")
plt.ylabel("True Positives")
plt.plot(s_vals,true_positives,'b')

plt.subplot(412)
plt.xlabel("Sigma")
plt.ylabel("False Positives")
plt.plot(s_vals,false_positives,'r')

plt.subplot(413)
plt.xlabel("Sigma")
plt.ylabel("False Negatives")
plt.plot(s_vals,false_negatives,'m')

plt.subplot(414)
plt.xlabel("Sigma")
plt.ylabel("True Negatives")
plt.plot(s_vals,true_negatives,'g')

#show figures
plt.show()