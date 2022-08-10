import time, math, random
import matplotlib.pyplot as plt

class Pathly:
	def __init__(self):
		self.min_length = 1
		self.max_length = 100
		self.vertice_count = 1000
		self.max_edges = 100
		self.load_graph()

	def run(self):
		start = '1'
		ends = ['7', '37', '59', '82', '99', '115', '133', '165', '188', '197']
		distances = []
		for end in ends:
			distance = self.dijkstra_algorithm(self.graph, start, end)
			distances.append(str(distance))
		print(f"Shortest paths found: {','.join(distances)}")

	def run_test(self):
		start = '1'
		end = '5'
		graph = {'1':[['2', 2], ['3', 1]],
					'2':[['4', 2]],
					'3':[['4', 1]],
					'4':[['5', 1]],
					'5':[]}
		distance = self.dijkstra_algorithm(graph, start, end)
		print(f'Shortest distance found of {distance}')

	def dijkstra_algorithm(self, graph, start, end): # Algorithm for finding shortest path in a directed graph with no negative edge lengths
		print(f"Searching for shortest path between {start} and {end}")
		current_node = start # Declare current node
		current_distance = 0 # Declare current distance

		distances = {node:float('inf') if node != start else current_distance for node in graph.keys()}# Declare hold variable for distances
		unvisited = {node:float('inf') if node != start else current_distance for node in graph.keys()}# Declare unvisited
		visited = [start]# Declare visited
		while unvisited: # loop through while their are still unvisited nodes * Could change to stop at a specific node
			for edge in graph[current_node]: # Iterate through all of the nodes edges
				if edge[0] not in visited: # If the node has not been previously visited
					distance = current_distance + edge[1]# Calculate the nodes tentative distance
					if distance < distances[edge[0]]: # If the tentative distance is shorter than it's current distance
						distances[edge[0]] = distance # Replace the distance with the new found shorter distance
						unvisited[edge[0]] = distance
			visited.append(current_node) # Mark the current node as visited
			del unvisited[current_node] # Remove the current node from the unvisited graph
			if len(unvisited) == 0: break
			min_distance = min(unvisited.values()) # Find the closest unvisited node
			for node, distance in unvisited.items():
				if distance == min_distance:
					current_node = node
					current_distance = min_distance
					break
		print(f"Shortest path found to be {distances[end]}")
		return distances[end]

	def generate_graph(self):
		self.graph = {str(x):[[str(sample), random.randint(self.min_length, self.max_length) ] for sample in random.sample(range(1, self.vertice_count + 1), self.max_edges) if sample != x ] for x in range(1, self.vertice_count + 1)}

	def load_graph(self):
		f = open('dijkstraData.txt', 'r')
		content = f.read()
		lines = content.split('\n')
		lines = [line.split('\t') for line in lines] # Split each lines
		self.graph = {str(line[0]):[[str(item.split(',')[0]), int(item.split(',')[1])] for item in line[1:-1]] for line in lines[:-1]} # Add each line into a dictionary entry
