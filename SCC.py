import time, math, random, sys, threading
import matplotlib.pyplot as plt
from collections import deque, defaultdict

class Graphly:
	# Graph search algorithms that run in O(m + n)/linear Time
	def __init__(self):
		#threading.stack_size(67108864)
		#sys.setrecursionlimit(2 ** 20)
		self.vertice_count = 10
		self.max_edges = 5

# -------------------- Strongly Connected Components Function  ---------------------- #
	def SCC_DFS(self):
		# Based on Kosaraju's two-pass algorithm for finding strongly connected components in O(m + n) speed!
		earlier = time.time()
		graph, reversed_graph, n = self.load_assignment_list()
		leaders, times = self.DFS_iter(reversed_graph, range(0, n), n)
		sorted_times = sorted(times, key=times.get, reverse = True)
		leaders, times = self.DFS_iter(graph, sorted_times, n)
		later = time.time()
		print(f"SCC script complete on graph of size {len(graph)} in {(later - earlier)} seconds")
		self.assess_clusters(leaders)
		return


	def DFS_iter(self, graph, nodes, n):
		times = {}
		leaders = {}
		current_time = 0
		explored = [False]*(n + 1)
		stack = []

		for node in nodes:
			if (not explored[node]):
				stack.append(node)
				while stack:
					stack_node = stack[-1]
					if (not explored[stack_node]):
						explored[stack_node] = True
						try:
							leaders[node].append(stack_node)
						except:
							leaders[node] = [stack_node]
						for neighbour in graph[stack_node]:
							if (not explored[neighbour]):
								stack.append(neighbour)
					else:
						stack_node = stack.pop()
						current_time += 1
						times[stack_node] = current_time
		return leaders, times



# ---------------------- Recursive Depth-First Search ----------------------#
	def DFS_recu(self, graph, node):
		self.bucketlist[node] = True
		for edge in graph[node]:
			if self.bucketlist[edge] != True:
				self.DFS_recu(graph, edge)

	def DFS_recu_loop(self, graph, node):
		self.bucketlist[node] = True
		self.leaders[self.leader].append(node)
		for edge in graph[node]:
			if self.bucketlist[edge] != True:
				self.DFS_recu_loop(graph, edge)
		self.timing += 1
		self.timings[self.timing] = node

# -------------------- Breadth-First Search --------------------------#

	def BFS(self, graph, start, bucketlist = None):
		# Breadth-First Search - A kind of cautious search
		queue = [start] # Establish a queue
		if bucketlist == None:
			bucketlist = {key:False for key in graph.keys()}
		bucketlist[start] = True # Mark starting position as explored
		while len(queue) != 0:
			v = queue.pop(0) # Remove first node of queue
			for w in graph[v]: # For each edge
				if bucketlist[w] == False: # If unexplored
					bucketlist[w] = True
					queue.append(w)
		return bucketlist

	def BFS_UC(self, graph):
		# Breadth-First Search for finding undirected connectivity and clusters
		bucketlist = {key:False for key in graph.keys()}
		clusters = 0
		for i in range(1, self.vertice_count + 1):
			if bucketlist[str(i)] == False:
				bucketlist = self.BFS(graph, str(i), bucketlist)
				clusters += 1
		return clusters

	def BFS_SP(self, graph, start):
		# Breadth-First Search to find the shortest path
		shortest_path = 0
		queue = [start] # Establish a queue

		bucketlist = {key:False for key in graph.keys()}
		bucketlist[start] = True # Mark starting position as explored

		distances = {key:0 if key == start else float('inf') for key in graph.keys()}
		while len(queue) != 0:
			v = queue.pop(0) # Remove first node of queue
			for w in graph[v]: # For each edge
				if bucketlist[w] == False: # If unexplored
					distances[w] = distances[v] + 1
					bucketlist[w] = True
					queue.append(w)
		return v, distances[v]
# ------------------------ Graph Pre/Post Processing ------------------#
	def generate_graph(self):
		self.graph = {str(x):[str(sample) for sample in random.sample(range(1, self.vertice_count + 1), self.max_edges) if sample != x ] for x in range(1, self.vertice_count + 1)}

	def load_assignment_list(self):
		with open('SCC.txt', 'r', newline = '\n') as f:
			lines = [line.split() for line in f.readlines()]
		m = len(lines)
		Vs_n = set(int(row[0]) for row in lines)
		Vs_m = set(int(row[1]) for row in lines)
		Vs = Vs_m.union(Vs_n)

		n = len(Vs)
		graph = [[] for i in range(n + 1)]
		reversed_graph = [[] for i in range(n + 1)]

		for items in lines:
			graph[int(items[0])] += [int(items[1])]
			reversed_graph[int(items[1])] += [int(items[0])]
		return graph, reversed_graph, n

	def load_assignment_graph(self):
		graph = {}
		data = open('SCC.txt', 'r').read().split('\n')
		biggest_node = 0
		for datum in data:
			edge = datum.split(' ')
			if int(edge[1]) > biggest_node:
				biggest_node = int(edge[1])
			try:
				graph[edge[0]].append(edge[1])
			except:
				graph[edge[0]] = [edge[1]]
		return graph, biggest_node

	def reverse_graph(self, graph): # Naive way to reverse a graph
		new_graph = {key:[] for key in graph.keys()}
		for node, edges in graph.items():
			for ind, edge in enumerate(edges):
				new_node = graph[node][ind]
				try:
					new_graph[new_node].append(node)
				except:
					new_graph[new_node] = [node]
		return new_graph

	def assess_clusters(self, leaders):
		print(f"Finding biggest clusters...")
		largest = [0]
		largest_leaders = [0]
		for leader, cluster in leaders.items():
			bigger = False
			for size in largest:
				if len(cluster) > size:
					bigger = True
			if bigger == True:
				largest.append(len(cluster))
				largest_leaders.append(leader)
				zipper = zip(list(largest), list(largest_leaders))
				zipper = sorted(zipper)
				largest, largest_leaders = list(zip(*zipper))
				largest, largest_leaders = list(largest), list(largest_leaders)
			if len(largest) > 5:
				largest.pop(0)
				largest_leaders.pop(0)
		for size, leader in zip(largest, largest_leaders):
			print(f"Cluster leader {leader} with size of {size} nodes")

# --------------------------------------------------- #
