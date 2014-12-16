import itertools, random, time, matplotlib,sys
import matplotlib.pyplot as plt
import dynamic_weights

Num_cities=raw_input('Enter number of cities')
priority = 0
City = complex


"""
You cannot apply the algorithm on a set of random cities and on a graph entred by yousimultaneously. If you choose 'Other set' as the option, the algorithm would be applied only to the new graph you enter and one should not expect the algorithm to proceed from the random set of cities they initially had generated.
But, one can always change weight patterns for the two weight patterns for the same graph entered by the user and expect the algorithm to continue frm the previos weight pattern.

"""

def set_nodes(Num):
	global nodes
	for x in xrange(Num):
		nodes=set(City(random.randrange(1,890), random.randrange(1,590)) for x in range(Num))
	print(nodes)
	return nodes

def choose_priority(chng_prior=False):
	print('Enter the set you wish to use from among the following.')
	print('1. Distance between two points')
	print('2. Distance d/2 between two points')
	print('3. Other set. (Not functional as yet.)')
	global prior
	prior=0
	prior=int(raw_input())
	global graph
	if prior==3:
		chng_graph=str(raw_input('Want to enter graph? (Enter Y or N for Yes or No)'))
		if chng_graph=='Y' or chng_graph=='y':
			graph=graph_input()
			#choose_algo()
		#elif chng_graph=='N' or chng_graph=='n' and chng_prior==False:
			#choose_algo()
		else:
			pass
	if chng_prior==False:
		if prior==1 or prior==2:
			choose_algo()
		else:
			print('Wrong choice. Aborting.')
			exit(0)

def graph_input():
	global V
	global E
	V = int(raw_input("Enter the number of Nodes: "))
	E = int(raw_input("Enter the number of Edges: "))

	print("Enter Edges with weights")
	print("Enter in the following format - 'start_node' 'end_node' 'edge_weight':")

	global adj_matrix
	global adj_matrix1
	global adj_matrix2
	adj_matrix = []
	adj_matrix1 = []
	adj_matrix2 = []

	for i in range(0, V):
		temp = []
		for j in range(0, V):
			temp.append(0)
		adj_matrix.append(temp)
		adj_matrix1.append(temp)
		adj_matrix2.append(temp)
	
	adj_matrix1=create_matrix(V, E)
	print('Enter another set of weights for the same matrix.')
	adj_matrix2=create_matrix(V, E)

 	print('adj_matrix1:')
	for i in range (0, V):
		print adj_matrix1[i]
	print('adj_matrix2:')
	for i in range(0,V):
		print adj_matrix2[i]

	adj_matrix=choose_matrix()
	print('The matrix you have chosen is:\n')
	for i in range(0,V):
		print adj_matrix[i]
	choose_algo()
	return adj_matrix

def create_matrix(V, E):
	global created
	created=[]

	for i in range(0, V):
		temp = []
		for j in range(0, V):
			temp.append(0)
		created.append(temp)

	for i in range(0, E):
		s = raw_input()
		u, v, w = s.split()
		u = int(u)
		v = int(v)
		w = int(w)
		created[v][u] = created[u][v] = w

	for i in range(0,V):
		print created[i]
	return(created)

def choose_matrix():
	mat=raw_input('What matrix do you wish to use? Enter 1 or 2.')
	if mat=='1':
		return(adj_matrix1)
	elif mat=='2':
		return(adj_matrix2)
	else:
		print("You have chosen a matrix that doesn't exist. Aborting")
		exit(0)

def choose_algo():
	print('Choose one of the following Algorithms you wish to apply and enter the corresponding number:\n')
	print('1. Naive TSP\n')
	print('2. Greedy TSP\n')
	print('3. Greedy Naive End TSP\n')
	print('4. Greedy Both Ends Search TSP\n')
	print('5. Double Greedy TSP')
	print('(Refer to the source code for details of each of them)')
	global choice
	choice=int(raw_input())

def naive_tsp():
	paths=alltours()
	final_route=shortest(paths)		#final_route is a list
	print(final_route)
	return final_route

def greedy_tsp(start=None):
	if start is None:
		start=first()
	tour = [start]
	#free are the nodes that are not visited yet
	free=nodes-{start}
	while free:
		a=nearest(tour[-1], free)
		#print(a)
		tour.append(a)
		free.remove(a)
		print(tour)
	return tour

def all_greedy_tsp():
	return shortest(greedy_tsp(nodes, start=c) for c in nodes)

def greedy_tsp_graph(start=0):
	graph=choose_matrix()
	tour1=[0]
	for i in range(len(graph)):
		tour=input1.greedy_tsp(graph, tour1)
		tour1=tour
		if len(tour1)==len(graph):
			break
		else:
			graph=choose_matrix()
			continue
	return tour

def greedy_naive_end(start=None, end_size=10):
	if start is None:
		start=first()
	tour= [start]
	free=nodes-{start}
	while len(free) > end_size:
		a=nearest(tour[-1], free)
		tour.append(a)
		free.remove(a)
		print(tour)
	#shortest_end - the shortest path to the naive approach applied to 'end_size' number of nodes
	exacts=map(list, itertools.permutations(free))
	shortest_end=shortest([tour[0], tour[-1]] + exact for exact in exacts)
	final=tour+shortest_end[2:]
	return final

def both_ends_greedy(begin_size=9, end_size=10):
	begins=random.sample(nodes, min(len(nodes), begin_size))
	return shortest(greedy_naive_end(begin, end_size) for begin in begins)

def double_greedy_tsp(start=None):
	NearestNeighbour = {T: nearest(T, nodes-{T}) for T in nodes}
	if start is None:
		start=first()
	tour=[start]
	free=nodes-{start}
	while free:
		Last = tour[-1]
		if NearestNeighbour[Last] is free:
			B = NearestNeighbour[Last]
		else:
			B = nearest(Last, free)
		Ds= [D for D in free if NearestNeighbour[D] is Last and D is not B]
		#for D in free:
		#	if NearestNeighbour[D] is Last and D is not B:
		#		Ds=D
		if Ds:
			T = min(Ds, key=lambda D: weight(D, Last))
		else:
			T = B
		tour.append(T)
		free.remove(T)
	return tour

def nearest(A, free):
	global chng_prior
	chng_prior=str(raw_input('Want to change priority of weight patterns? (Enter Y or N for Yes or No)'))
	if chng_prior=='Y' or chng_prior=='y':
		chng_prior=True
		choose_priority()
	elif chng_prior=='N' or chng_prior=='n':
		chng_prior=False
	else:
		pass
	xyz=min(free, key=lambda x: weight(x, A))
	return xyz

def alltours():
	start=first()
	for tour in itertools.permutations(nodes-{start}):
		return [[start] + list(tour)]

def first():
	for city in nodes:
		return city

def shortest(paths):
	return min(paths, key=total_distance)

def total_distance(path):
	total=sum(weight(path[i], path[i-1]) for i in range(len(path)))
	print(total)
	return total

def weight(start, end):
	if prior==1:
		dis=abs(start-end)
		return dis
	elif prior==2:
		dis=abs((start-end)/2)
		return dis
	elif prior==0:
		print('Please select a priority.')
		exit(0)
	else:
		print('Wrong Priority.')
		exit(0)

def plot_tour():
	t1=time.clock()
	if choice==1:
		name='naive_tsp'
		tour=naive_tsp()
	elif choice==2:
		if prior==3:
			name='greedy_tsp_graph'
			tour=greedy_tsp_graph(adj_matrix)
			print(tour)
			exit(0)
		else:
			name='greedy_tsp'
			tour=greedy_tsp()
	elif choice==3:
		name='greedy_naive_end'
		tour=greedy_naive_end()
	elif choice==4:
		name='both_ends_greedy'
		tour=both_ends_greedy()
	elif choice==5:
		name='double_greedy_tsp'
		tour=double_greedy_tsp()
	else:
		print('Please choose one of the above to proceed.')
	t2=time.clock()
	print(list(tour)+[tour[0]])
	plotline(list(tour)+[tour[0]])
	plotline([tour[0]], 'rs')
	plt.show()
	print("{} city tour; total_distance={:.1f}; time={:,.3f} secs for {}".format(
			len(tour), total_distance(tour), t2-t1, name))

def plotline(points, style='bo-'):
	X,Y = XY(points)
	plt.plot(X, Y, style)

def XY(points):
	return [p.real for p in points], [p.imag for p in points]

set_nodes(int(Num_cities))
choose_priority()
plot_tour()