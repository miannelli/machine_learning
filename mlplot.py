import tablemaker as tm
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
from statistics import mean

'''
Keyword Arguments: 
	error - Named column for error bars, default None
	xscale - Scale for x-axis, default "log"
	save - True if the plots should be saved, False if displayed (default False)
	name - name to be used for the first part of the filename to save plots to. If
		plot_file was called and no name was specified, name defaults to the filename.
		If no name was specified and plot_file wasn't called, the default is "ML_Plot"
	agg_func - For data which needs to be aggregated, the function to use to aggregate
		the data, default is mean
'''

'''
function bar_plot_data:
	headers - a list containing the names for each column of data
	data - the list of lists, containing data that matches the headers
	x - the header of the data that should be on the x-axis, e.g., "N"
	y - the header of the data that should be on the y-axis, e.g., "Mean"
	bar_group - the header of the data that should be used to group x,y data into a single
		bar per value on the graph, e.g., "Metric"
	plot_group - the header of the data that should be used to group x,y data into
		separate plots per value, e.g., "K"
	error - the header of the data that should be used for error bars for each bar,
		e.g., "StandardDeviation"
'''
def bar_plot_data(headers,data,x,y,bar_group,plot_group,**kwargs):
	#default values
	if not 'xscale' in kwargs:
		xscale = 'log'
	else:
		xscale = kwargs['xscale']
	if not 'error' in kwargs:
		error = None
	else:
		error = kwargs['error']
	if not 'save' in kwargs:
		save = False
	else:
		save = kwargs['save']
	if not 'name' in kwargs:
		name = "ML_Plot"
	else:
		name = kwargs['name']
	
	
	#determine headers
	index_x = headers.index(x)
	index_y = headers.index(y)
	if error is not None: index_error = headers.index(error)
	index_group = headers.index(plot_group)
	index_bar = headers.index(bar_group)
	
	zipped=[list (z) for z in zip(*data)]
	plot_group_by = sorted(set(zipped[index_group]))
	bar_group_by = sorted(set(zipped[index_bar]))
	x_values = sorted(set(zipped[index_x]))
	
	#plot stuff
	bar_width=.25
	group_width = .25
	colors = ["red","green","blue","black"]
	num_colors = len(colors)
	ind = np.arange(len(x_values))

	for p_group in plot_group_by:
		bars = []
		fig, sp = plt.subplots()
		grouped_data = [list (f) for f in filter(lambda x: x[index_group] == p_group, data)]
		group_zipped = [list (z) for z in zip(*grouped_data)]
			
		for i in range(len(bar_group_by)):
			b_group=bar_group_by[i]
			bar_data = [list (f) for f in filter(lambda x: x[index_bar] == b_group, grouped_data)]
			bar_zipped = [list (z) for z in zip(*bar_data)]
		
			if error is not None:
				#list(map(lambda x: int(x) + (bar_width*i),bar_zipped[index_x]))
				bars.append(sp.bar([j + bar_width*i for j in ind],
					bar_zipped[index_y],
					group_width,
					yerr=bar_zipped[index_error],
					color=colors[i%num_colors],
					error_kw= {'ecolor': 'black', 'capsize': 3, 'elinewidth': 2}))
			else:
				bars.append(sp.bar([j + bar_width*i for j in ind],
					bar_zipped[index_y],
					group_width,
					color=colors[i%num_colors]))
		#label bars
		sp.legend([b[0] for b in bars],bar_group_by,loc=2)
		sp.set_ylabel(headers[index_y])
		sp.set_xlabel(headers[index_x])
		plt.xlim(min(ind)-bar_width, max(ind)+bar_width*4)
		sp.set_title(plot_group+"="+str(p_group))
		sp.set_xticks(ind + bar_width*len(bar_group_by))
		sp.set_xticklabels(x_values)
		
		plt.plot()
		
		if save:
			filename = "plots/" + name + "-" + str(p_group) + "-" + str(b_group)+".png"
			plt.savefig(filename)
		else:
				plt.show()
		
		plt.close()

'''reads a previously saved table from the file, then plot the data'''
def bar_plot_file(file,x,y,bar_group,plot_group,**kwargs):
	(headers, data) = tm.read_table(file)
	if not 'name' in kwargs:
		kwargs['name']=file

	bar_plot_data(headers,data,x,y,bar_group,plot_group,**kwargs)

'''
function scatter_plot_data:
	headers - a list containing the names for each column of data
	data - the list of lists, containing data that matches the headers
	x - the header of the data that should be on the x-axis, e.g., "N"
	y - the header of the data that should be on the y-axis, e.g., "Accuracy"
'''	
def scatter_plot_data(headers,data,x,y,**kwargs):
	#default values
	if not 'xscale' in kwargs:
		xscale = 'log'
	else:
		xscale = kwargs['xscale']
	if not 'save' in kwargs:
		save = False
	else:
		save = kwargs['save']
	if not 'name' in kwargs:
		name = "ML_Plot"
	else:
		name = kwargs['name']
	
	
	#determine headers
	index_x = headers.index(x)
	index_y = headers.index(y)
	
	zipped=[list (z) for z in zip(*data)]
	x_values = zipped[index_x]
	y_values = zipped[index_y]
	
	fig, sp = plt.subplots()
	sp.scatter(x_values, y_values, c="blue", alpha=0.3, edgecolors='none')
	sp.set_ylabel(headers[index_y])
	sp.set_xlabel(headers[index_x])
	sp.set_title(headers[index_y] + " vs. " + headers[index_x])
	#plt.legend(loc=2)
	sp.grid(True)

	plt.plot()
	plt.xlim(min(x_values),max(x_values))
	plt.ylim(min(y_values),max(y_values))
	
	if save:
		filename = "plots/" + name + "-" + headers[index_y] + " vs. " + headers[index_x]+".png"
		plt.savefig(filename)
	else:
		plt.show()
	plt.close()

'''reads a previously saved table from the file, then plot the data'''
def scatter_plot_file(file,x,y,**kwargs):
	(headers, data) = tm.read_table(file)
	if not 'name' in kwargs:
		kwargs['name']=file

	scatter_plot_data(headers,data,x,y,**kwargs)
'''
function aggr_scatter_plot_data:
	headers - a list containing the names for each column of data
	data - the list of lists, containing data that matches the headers
	x - the header of the data that should be on the x-axis, e.g., "N"
	y - the header of the data that should be on the y-axis, e.g., "Accuracy"
	group_by_headers - a list containing the headers to group the data by, e.g.,
		['K','sigma']
	group_by_vals - a list of values which are used to select a specific group of data,
		e.g., [500,.05]
'''	
def aggr_scatter_plot_data(headers,data,x,y,group_by_headers,group_by_vals,**kwargs):
	#default values
	if not 'xscale' in kwargs:
		xscale = 'log'
	else:
		xscale = kwargs['xscale']
	if not 'save' in kwargs:
		save = False
	else:
		save = kwargs['save']
	if not 'name' in kwargs:
		name = "ML_Plot"
	else:
		name = kwargs['name']
	if not 'linreg' in kwargs:
		linreg=False
	else:
		linreg=True
	if not 'agg_func' in kwargs:
		agg_func=mean
	else:
		agg_func=kwargs['agg_func']
		
	#determine headers
	index_x = headers.index(x)
	index_y = headers.index(y)
	index_group = [headers.index(g) for g in group_by_headers]

	#filter data to only include data which match each group_by_header on group_by_vals, the select only the x,y values
	filtered_data = [itemgetter(index_x,index_y)(f) for f in filter(lambda x: itemgetter(*index_group)(x)==tuple(group_by_vals),data)]	

	#exit if no matched data
	if not filtered_data:
		print("Error: No data matching "+",".join(map(str,group_by_headers)) +"="+ ",".join(map(str,group_by_vals))+" found.")
		return
	
	zipped=[list (z) for z in zip(*filtered_data)]
	#get unique x values
	x_values = sorted(set(zipped[0]))
	#aggregate y values
	y_values = [agg_func(f[1] for f in filter(lambda x: x[0] == x_value,filtered_data)) for x_value in x_values]	
	
	fig, sp = plt.subplots()
	sp.set_ylabel(headers[index_y])
	sp.set_xlabel(headers[index_x])
	
	#generate title
	grouped_title=",".join([" For "+str(group_by_headers[i])+"="+str(group_by_vals[i]) for i in range(len(group_by_headers))])
	sp.set_title(headers[index_y] + " vs. " + headers[index_x]+"\n"+grouped_title)
		
	#plt.legend(loc=2)
	sp.grid(True)
	
	#if linreg was specified, plot a linear regression
	if linreg:
		z = np.polyfit(x_values, y_values, 1)
		f = np.poly1d(z)

		# calculate new x's and y's
		x_new = np.linspace(x_values[0], x_values[-1], 50)
		y_new = f(x_new)
		plt.plot(x_values,y_values,'o', x_new, y_new)	
	else:
		sp.scatter(x_values, y_values, c="blue", edgecolors='none')
		
	plt.plot()
	
	#add some space around the max,min values
	ratio = .05
	x_avg = mean(x_values)
	y_avg = mean(y_values)
	plt.xlim(min(x_values)-(ratio*x_avg),max(x_values)+(ratio*x_avg))
	plt.ylim(min(y_values)-(ratio*y_avg),max(y_values)+(ratio*y_avg))
	
	if save:
		filename = "plots/" + name + "-" + headers[index_y] + " vs. " + headers[index_x]+grouped_title+".png"
		plt.savefig(filename)
	else:
		plt.show()
	plt.close()

'''reads a previously saved table from the file, then plot the data'''
def aggr_scatter_plot_file(file,x,y,group_by_headers,group_by_vals,**kwargs):
	(headers, data) = tm.read_table(file)
	if not 'name' in kwargs:
		kwargs['name']=file

	aggr_scatter_plot_data(headers,data,x,y,group_by_headers,group_by_vals,**kwargs)
'''
function aggr_bar_plot_data:
	headers - a list containing the names for each column of data
	data - the list of lists, containing data that matches the headers
	x - the header of the data that should be on the x-axis, e.g., "N"
	y - the header of the data that should be on the y-axis, e.g., "Mean"
	bar_group - the header of the data that should be used to group x,y data into a single
		bar per value on the graph, e.g., "Metric"
	group_by_headers - a list containing the headers to group the data by, e.g.,
		['K']
	group_by_vals - a list of values which are used to select a specific group of data,
		e.g., [500]	
	error - the header of the data that should be used for error bars for each bar,
		e.g., "StandardDeviation"
'''

def aggr_bar_plot_data(headers,data,x,y,bar_group,group_by_headers,group_by_vals,**kwargs):
	#default values
	if not 'xscale' in kwargs:
		xscale = 'log'
	else:
		xscale = kwargs['xscale']
	if not 'error' in kwargs:
		error = None
	else:
		error = kwargs['error']
	if not 'save' in kwargs:
		save = False
	else:
		save = kwargs['save']
	if not 'name' in kwargs:
		name = "ML_Plot"
	else:
		name = kwargs['name']
	if not 'agg_func' in kwargs:
		agg_func=mean
	else:
		agg_func=kwargs['agg_func']
	
	#determine headers
	index_x = headers.index(x)
	index_y = headers.index(y)
	if error is not None: index_error = headers.index(error)
	index_bar = headers.index(bar_group)
	index_group_by = [headers.index(g) for g in group_by_headers]

	#filter data to only include data which match each group_by_header on group_by_vals, the select only the x,y values
	if len(index_group_by) > 1:
		filtered_data = [list(f) for f in filter(lambda x: itemgetter(*index_group_by)(x)==tuple(group_by_vals),data)]
	else:
		filtered_data = [list(f) for f in filter(lambda x: x[index_group_by[0]]==group_by_vals[0],data)]	

	#exit if no matched data
	if not filtered_data:
		print("Error: No data matching "+",".join(map(str,group_by_headers)) +"="+ ",".join(map(str,group_by_vals))+" found.")
		return
		
	zipped=[list (z) for z in zip(*filtered_data)]
	#list of unique bar values
	bar_group_by = sorted(set(zipped[index_bar]))
	#list of unique x values
	x_values = sorted(set(zipped[index_x]))
	
	#plot stuff
	bar_width=.25
	group_width = .25
	colors = ["red","green","blue","black"]
	num_colors = len(colors)
	#creates a list to index each x_value on the plot
	ind = np.arange(len(x_values))
	fig, sp = plt.subplots()
	bars=[]
	
	#generate the plot for each bar_group (e.g., 'Metric')
	for i in range(len(bar_group_by)):
		b_group=bar_group_by[i]
		#filter the data for this bar group
		bar_data = [list(f) for f in filter(lambda x: x[index_bar] == b_group, filtered_data)]
		#aggregate bar values
		bar_values = [agg_func(f[index_y] for f in filter(lambda x: x[index_x] == x_value,bar_data)) for x_value in x_values]	
		
		#if error, print error bars
		if error is not None:
			error_values = [agg_func(f[index_error] for f in filter(lambda x: x[index_x] == x_value,bar_data)) for x_value in x_values]	
			bars.append(sp.bar([j + bar_width*i for j in ind],
				bar_values,
				group_width,
				yerr=error_values,
				color=colors[i%num_colors],
				error_kw= {'ecolor': 'black', 'capsize': 3, 'elinewidth': 2}))
		else:
			bars.append(sp.bar([j + bar_width*i for j in ind],
				bar_values,
				group_width,
				color=colors[i%num_colors]))
	#label bars, title, etc
	sp.legend([b[0] for b in bars],bar_group_by,loc=2)
	sp.set_ylabel(headers[index_y])
	sp.set_xlabel(headers[index_x])
	plt.xlim(min(ind)-bar_width, max(ind)+bar_width*4)
	grouped_title=",".join([" For "+str(group_by_headers[i])+"="+str(group_by_vals[i]) for i in range(len(group_by_headers))])
	sp.set_title(grouped_title)
	sp.set_xticks(ind + bar_width*len(bar_group_by))
	sp.set_xticklabels(x_values)
	
	#generate the plot
	plt.plot()
	
	if save:
		filename = "plots/" + name + "-"+ grouped_title+".png"
		plt.savefig(filename)
	else:
			plt.show()
	
	plt.close()

'''reads a previously saved table from the file, then plot the data'''
def aggr_bar_plot_file(file,x,y,bar_group,group_by_headers,group_by_vals,**kwargs):
	(headers, data) = tm.read_table(file)
	if not 'name' in kwargs:
		kwargs['name']=file

	aggr_bar_plot_data(headers,data,x,y,bar_group,group_by_headers,group_by_vals,**kwargs)




