#!/opt/local/bin/python3.4

'''
Jonathan Gryak
Machine Learning, Fall 2015
Exercise 1
'''

#import packages

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import spatial

k=5


curr_dist = np.random.uniform

# generate num_points points (vectors) of length dim with values provided by function dist
def generatePoints(num_points, dim, dist, min, max):
	points = np.empty([num_points,dim])
	for i in range(0,num_points):
		for j in range(0,dim):
			points[i][j]=curr_dist(min,max)
	return points

#calculate min and max distance from point to other_points, using distance function

def calcDistance(point,other_points,metric):
	op_list=other_points.tolist()
	curr_min = float("inf")
	curr_max = 0
	for op in op_list:
		dist = metric(point,op)
		if curr_min > dist:
			curr_min=dist
		if curr_max < dist:
			curr_max=dist
	return curr_min,curr_max
	
#creates a mask for slicing a numpy array which removes the element at omit_pos
def ndslice(omit_pos,len):
	mask = [True for i in range(0,len)]
	mask[omit_pos]=False
	return mask

#calculate average of the ratio of Dmin/Dmax
def avgDRatio(k,curr_samples,curr_metric):
	#first r-value
	op = np.compress(ndslice(0,k),curr_samples,axis=0)
	cmin,cmax = calcDistance(curr_samples[0],op,curr_metric)
	#print(cmin/cmax)
	r_average = cmin/cmax

	#calculate average r
	for i in range(1,k):
		#print("Point: ",curr_samples[i])
		#print("Other Points:",np.compress(ndslice(i,n),curr_samples,axis=0))
		op = np.compress(ndslice(i,k),curr_samples,axis=0)
		cmin,cmax = calcDistance(curr_samples[i],op,curr_metric)
		#print(cmin/cmax)
		r_average = ((cmin/cmax)+i*r_average)/(i+1)
	#return 
	return r_average

#generate samples
#samples = generatePoints(k,n,curr_dist,0,1)

#test out
#print("Samples:",samples)

#metric array
metrics = [[spatial.distance.cityblock,"L1"],[spatial.distance.euclidean,"L2"],[spatial.distance.chebyshev,"LI"]]

n_vals= list(range(1,11)) + list(range(20,110,10))
#print(n_vals)
#store results
r_vals=[[0 for x in range(len(n_vals))] for y in range(len(metrics))]
#print(r_vals)
r_stds=[0 for x in range(len(metrics))]

#run experiment 1
#for each metric
for i in range(0,len(metrics)):
	#for each dimension value
	for j in range(0,len(n_vals)):
		#generate k points of dimension n_vals[j], selecting values from the uniform
		#distribution on [0,1]
		samples=generatePoints(k,n_vals[j],curr_dist,0,1)
		#calculate the average distance ratio for each set of points
		r_vals[i][j]= avgDRatio(k,samples,metrics[i][0])
	#print("For metric ",metrics[i][1],r_vals[i])
	#calculate the standard deviation for this set of points
	r_stds[i] = np.std(r_vals[i])
#	print("|r val|=",len(r_vals[i]),",|n val|=",len(r_vals))
	#plt.plot(n_vals,r_vals[i],label=metrics[i][1])
	plt.errorbar(n_vals,r_vals[i],r_stds[i],label=metrics[i][1]+"\ts:"+str(r_stds[i]))

#display graph
plt.xscale('log')
plt.legend(loc=3)
plt.title("K="+str(k))
plt.show()

