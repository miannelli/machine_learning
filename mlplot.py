import tablemaker as tm
import matplotlib.pyplot as plt
import numpy as np

'''
Keyword Arguments: 
	error - Named column for error bars, default None
	xscale - Scale for x-axis, default "log"
	save - True if the plots should be saved, False if displayed (default False)
	name - name to be used for the first part of the filename to save plots to. If
		plot_file was called and no name was specified, name defaults to the filename.
		If no name was specified and plot_file wasn't called, the default is "ML_Plot"
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





