import time, math, random
import matplotlib.pyplot as plt

class Contractor:
	def __init__(self):
		self.vertice_count = 10
		self.max_edges = 5

	def run(self):
		min_slices = []
		for x in range(1, 50):
			self.download_graph()
			min_slices.append(self.random_contract(self.graph))
		print(f'Minimum slice found - {min(min_slices)}')
		print(min_slices)

	def random_contract(self, graph):
		while len(graph.keys()) > 2:
			u = random.choice(list(graph)) # Pick an edge at random
			v = str(graph[u][random.randint(0, len(graph[u]) - 1)])
			uv = ' ' + u + ' ' + v + ' '
			graph[uv] = graph.pop(u) + graph.pop(v) # Combine the vertices into one point
			graph[uv] = [vertice for vertice in graph[uv] if self.pad(u) not in self.pad(vertice) and self.pad(v) not in self.pad(vertice)] # Delete self-loops
			graph = {vertice:[uv if self.pad(edge) in uv else edge for edge in edges] for vertice, edges in graph.items()} # Update pointers with new mega-node name
		return len(graph[uv])

	def intelligent_contract(self, graph):
		return

	def download_graph(self):
		f = open('vertices.txt', 'r')
		content = f.read().split('\n')
		content = [line.split('\t')[:-1] for line in content]
		content.pop()
		self.graph = {line[0]:[edge for edge in line[1:]] for line in content}

	def generate_graph(self):
		self.graph = {str(x):[str(sample) for sample in random.sample(range(1, self.vertice_count + 1), self.max_edges) if sample != x ] for x in range(1, self.vertice_count + 1)}

	def pad(self, string):
		return ' ' + string + ' '
