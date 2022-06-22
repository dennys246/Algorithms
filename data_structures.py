import random, math, time, hashlib


# ------------------- Hash Table ---------------------------------#
# Usually hash table used for super quick lookup times as well as
# insertion and deletions (constant time! O(1))
# Great for applications that require a lot of look ups
# Two types of Hash Tables below with varied collision resolution functions, (i.e. Chained and Open Addressed)
# Note on Hash Function itself: The hashing function is a bit of an art and design with vary
# Across developers. Key notes to remember is that the gold standard for a good hash function
# it will lead too good performance (i.e. spread data out evenly across buckets) and should be easy to both store
# AND access data. Very easy to develope a bad hash function so be sure to look at many examples
# in many contexts when developing a function for real life use!
#
# Quick-N-Dirty Hash Functions (Not to be used on mission critical stuff) -
# Convert object to integers via a "Hash code" (using subroutine to convert str to int)
# then use a "compression function" to access correct bucket
#
# How to choose n (i.e. number of buckets)? Some general guidelines being...
# 1 - Choose n to be a prime number (within constant factor of @ of object in table)
# 2 - Not to close to a power of 2
# 3 - Not too close to a power of 10
#
# Final Important Note - Do a lot of research and stress tests on optimal hash functions
# when creating a hash table on mission critical things. The below code may be a
# good start but again it is very easy to create a bad hash function that can even be exploited
# by bad actors. Consider using cryptographic hash functions (i.e. SHA-2) or use randomization
# by creating a number of hash functions to randomly select from at run time (allows for open-source!) ensuring
# pathological data set is impossible to reverse engineer or at minimum very ineffective.



class UniversalHashTable: # Open addressing is the way of resolving collisions in this class - Less memory required to utilize
	def __init__(self, data = None, empty = False):
		self.min_fill = float(1/3)
		self.max_fill = float(2/3)

		self.size = 0
		self.capacity = 2

		self.collision_count = 0

		self.primes = find_primes(1, 10)
		self.a = random.sample(self.primes, 1)[0]
		self.b = random.sample(self.primes, 1)[0]
		self.c = random.sample(self.primes, 1)[0]
		self.d = random.sample(self.primes, 1)[0]

		self.constant = random.uniform(0, 1)

		self.hasher = lambda key : self.sha3(key)
		self.prober = lambda key, hashkey : self.linear_probe(key, hashkey)

		self.table = [None]*self.capacity


        self.fill(data = data, empty = empty)
		if empty == False:
			self.double_check()

	def __repr__(self):
		return f"HashTable with {self.capacity} capacity {(self.size/self.capacity)*100}% full - {(self.collision_count/self.size)*100}% Collision Rate"

	# ------------- Hash Table Hash Functions --------------- #
	# Obsolete Hash Functions: MD5, SHA-1, SHA-2 (Not obsolete yet but a matter of time),

	def pyhash(self, key): # Uses a pythons inbuilt hash function which utilitzes SipHash
		# Avoid using this function for times when you have a lot of very close
		# values, especially integers, being inserted into a hash table to avoid primary clustering
		return hash(key) % self.capacity # Utilizes Add-Block-XOR Block Cipher

	def sha2(self, key): # Secure Hash Algorithm 2 - AVOID USING - Somewhat secure but most likely vulnerable
		return int.from_bytes(hashlib.sha512(self.encode(key)).digest(), 'little') % self.capacity

	def sha3(self, key): # Secure Hash Algorithm 3
		return int.from_bytes(hashlib.sha3_512(self.encode(key)).digest(), 'little') % self.capacity

	def blake2(self, key, subhash = 's'):
		if subhash == 's':
			return int.from_bytes(hashlib.blake2s(self.encode(key)).digest(), 'little') % self.capacity
		if subhash == 'b':
			return int.from_bytes(hashlib.blake2b(self.encode(key)).digest(), 'little') % self.capacity

	def linear_hash(self, key): # Don't think this is a real hash function
		return (self.a*sum(self.encode(key)) + self.b) % self.capacity

	def division_hash(self, key):
		return sum(self.encode(key)) % self.capacity

	def multiplication_hash(self, key):
		return math.floor(self.capacity*((sum(self.encode(key))*self.constant) % 1))

	def encode(self, key):
		return bytes(str(key), 'utf-8')

	# ------------ Hash Table Collision Probes -------------- #

	def linear_probe(self, key, hashkey, increment = True): # Probing function used for linear hashing
		self.collision_count += 1
		self.probe_count += 1
		return (5*hashkey + 1) % self.capacity
		#return (hashkey + 1) % self.capacity

	def quad_probe(self, key, hashkey, increment = True): # Probing function used for quadratic probing
		self.collision_count += 1
		self.probe_count += 1
		#hashkey = hashkey + (self.a*self.probe_count) + (self.b*(self.probe_count**2))
		hashkey = hashkey + (self.probe_count**2)
		return hashkey % self.capacity

	def double_probe(self, key, hashkey):
		self.collision_count += 1
		self.probe_count += 1
		hashkey = self.linear_probe(key, hashkey, False) + self.probe_count*self.quad_probe(key, hashkey, False)
		return hashkey % self.capacity

	# ------------- Core Hash Table Functions ------------- #

	def fill(self, data = None, replace = True, empty = False):
		if self.size != 0 and replace == True: # If data has already been added to the table, reset param/variables
			self.size = 0
			self.capacity = 2
			self.collision_count = 0

			self.table = [None]*self.capacity

		self.data = data
		if self.data == None and empty == False: self.data = [random_ip() for ip in range(100000)]
		if self.data != None:
			for datum in self.data:
				self.add(datum)
			self.__repr__()
		else:
			print('Empty universal hash table initialized')

	def add(self, key):
		fill = float(self.size/self.capacity)
		if self.min_fill > fill or fill > self.max_fill:
			self.resize()
		hashkey = self.hasher(key)
		while self.table[hashkey] is not None:
			if self.table[hashkey] == key: # If the key already exists in the table
				return# Return
			if self.table[hashkey] == '!tombstone!': # If a tombstone was found
				break # Replace tombstone
			hashkey = self.prober(key, hashkey)
		self.table[hashkey] = key # insert the new key into the found hash
		self.size += 1 # Increment size
		self.probe_count = 0 # Reset

	def search(self, key):
		hashkey = self.hasher(key)
		while self.table[hashkey] is not None:
			if self.table[hashkey] == key:
				return True
			hashkey = self.prober(key, hashkey)
		self.probe_count = 0 # Reset the quadratic multiplier probe for the next call
		return False

	def remove(self, key):
		hashkey = self.hasher(key)
		while self.table[hashkey]:
			if self.table[hashkey] == key:
				self.table[hashkey] = '!tombstone!'
				self.size -= 1
				break
			hashkey = self.prober(key, hashkey)
		if self.min_fill > float(self.size/self.capacity): # If table is bellow minimum fill
			self.resize() # resize
		self.probe_count = 0 # Reset the quadratic multiplier probe for the next call

	def resize(self):
		fill = float(self.size/self.capacity)
		old_capacity = self.capacity
		if self.min_fill > fill:
			self.capacity >>= 1
			print(f"Table below minimum fill, decreasing capacity to {self.capacity}")
		else:
			self.capacity <<= 1
			print(f"Table exceeding maximum fill, increasing capacity to {self.capacity}")
		new_table = [None]*self.capacity
		for ind in range(old_capacity):
			if self.table[ind] and self.table[ind] != '!tombstone!':
				position = self.hasher(self.table[ind])
				while new_table[position] is not None:
					position = self.prober(self.table[ind], position)
				new_table[position] = self.table[ind]
		self.table = new_table

	# ----------------- Excess Functions ----------------- #
	def double_check(self):
		found = 0
		for datum in self.data:
			if self.search(datum) == True:
				found += 1
		print(f"Double check found {(found/self.size)*100}% of data added")

class OAHashTable: # Using chaining to resolve collisions, Easier deletion process
	def __init__(self, data = None, empty = False):
		self.min_fill = float(1/3)
		self.max_fill = float(2/3)

		self.size = 0
		self.capacity = 2

		self.collision_count = 0

		self.primes = find_primes(1, 10)
		self.a = random.sample(self.primes, 1)[0]
		self.b = random.sample(self.primes, 1)[0]
		self.c = random.sample(self.primes, 1)[0]
		self.d = random.sample(self.primes, 1)[0]

		self.constant = random.uniform(0, 1)

		self.hasher = lambda key : self.pyhash(key)

		self.table = [[]]*self.capacity


		self.fill(data = data, empty = empty)
		if empty == False:
			self.double_check()


	def __repr__(self):
		return f"HashTable with {self.capacity} capacity {(self.size/self.capacity)*100}% full - {(self.collision_count/self.size)*100}% Collision Rate"

	def fill(self, data = None, replace = True, empty = False):
		if self.size != 0 and replace == True: # If data has already been added to the table, reset param/variables
			self.size = 0
			self.capacity = 2
			self.collision_count = 0

			self.table = [[]]*self.capacity

		self.data = data
		if self.data == None and empty == False: self.data = [random_ip() for ip in range(100000)]
		if self.data != None:
			for datum in self.data:
				self.add(datum)

		else:
			print('Empty universal hash table initialized')

	# ------------- Hash Table Hash Functions --------------- #
	# Obsolete Hash Functions: MD5, SHA-1, SHA-2 (Not obsolete yet but a matter of time),

	def encode(self, key):
		return bytes(str(key), 'utf-8')

	def pyhash(self, key): # Uses a pythons inbuilt hash function which utilitzes SipHash
		return hash(key) % self.capacity # Utilizes Add-Block-XOR Block Cipher

	def sha2(self, key): # Secure Hash Algorithm 2 - Somewhat secure but most likely vulnerable
		return int.from_bytes(hashlib.sha512(self.encode(key)).digest(), 'little') % self.capacity

	def sha3(self, key): # Secure Hash Algorithm 3
		return int.from_bytes(hashlib.sha3_512(self.encode(key)).digest(), 'little') % self.capacity

	def blake2(self, key, subhash = 's'):
		if subhash == 's':
			return int.from_bytes(hashlib.blake2s(self.encode(key)).digest(), 'little') % self.capacity
		if subhash == 'b':
			return int.from_bytes(hashlib.blake2b(self.encode(key)).digest(), 'little') % self.capacity

	def linear_hash(self, key): # Don't think this is a real hash function
		return (self.a*self.encode(key) + self.b) % self.capacity

	def division_hash(self, key):
		return self.encode(key) % self.capacity

	def multiplication_hash(self, key):
		return math.floor(self.capacity*((self.encode(key)*self.constant) % 1))



	# ------------- Core Hash Table Functions ------------- #

	def add(self, key):
		self.size += 1 # Increment size
		fill = float(self.size/self.capacity)
		if self.min_fill > fill or fill > self.max_fill:
			self.resize()
		hashkey = self.hasher(key)
		if key in self.table[hashkey]:
			return None
		else:
			self.table[hashkey].append(key)
		return key


	def remove(self, key):
		hashkey = self.hasher(key)
		if key in self.table[hashkey]:
			self.table[hashkey].remove(key)
			self.size -= 1
		if self.min_fill > float(self.size/self.capacity):
			self.resize()

	def search(self, key):
		hashkey = self.hasher(key)
		if key in self.table[hashkey]:
			return True
		else:
			return False

	def resize(self):
		fill = float(self.size/self.capacity)
		old_capacity = self.capacity
		if self.min_fill > fill:
			self.capacity >>= 1
			print(f"Table below minimum fill, decreasing capacity to {self.capacity}")
		else:
			self.capacity <<= 1
			print(f"Table exceeding maximum fill, increasing capacity to {self.capacity}")
		new_table = [[]]*self.capacity
		for data in self.table:
			for datum in data:
				if datum != '!tombstone!' and datum != None:
					hashkey = self.hasher(datum)
					new_table[hashkey].append(datum)
		self.table = new_table

	def double_check(self):
		found = 0
		for datum in self.data:
			if self.search(datum) == True:
				found += 1
		print(f"Double check found {(found/self.size)*100}% of data added")


# -------------------- Bloom Filter ----------------------------#
# Similar to a hash structure but lighter and faster, uses very small amount of memory
# and very fast inserts and lookups. The cons are that it can't store an associated
# object, cannot delete (some variants that do allow for deletions but complex)
# and their is a small false positive probability (however no posibility of false negative).
#
# Possible applications: Spellcheckers, assessing for too weak passwords, software on network
# routers that transfer packets of data (huge budget on space obviously and need fast data structure)

class BloomFilter:
	def __init__(self):
		return

	def __repr__(self):
		return 'something'

	def insert(self, value):
		return

	def search(self, value):
		return


# -------------------- Vanilla Binary Search Tree ---------------------#
# This vanilla binary search tree is a plain binary with all of the associated functions
# that can normally be performed on a binary search tree. Has the potential to
# not be well formed (i.e. a long single chain) causing long run times on occasionale
class BinaryTree:
	def __init__(self, values = None):
		if values == None: values = random.sample(range(1, 10), 9)
		self.root = Node(None, values.pop(0))
		self.batch_insert(values)

	def __repr__(self):
		return f"Root Value: {self.root.value}"

	def insert(self, value):
		node = self.root # Grab the root
		while node != None:
			if node.value >= value: # If the node value is larger than or equal too (too allow for duplicates) the value inserting
				if node.left == None:
					node.left = Node(node, value)
					break
				else:
					node = node.left
			else: # If the node is smaller than the value
				if node.right == None:
					node.right = Node(node, value)
					break
				else:
					node = node.right

	def batch_insert(self, values):
		for value in values:
			self.insert(value)
		return

	def search(self, value):
		node = self.root # Grab the root
		while node != None and node.value != value: # While we haven't found the node and we haven't found a dead end
			if node.value > value: # If the value is smaller than the node
				node = node.left # move down on left side of node
			else: # Else if it's larger
				node = node.right # Move down right side of tree
		return node # Return node

	def max(self):
		node = self.root # Grab the root
		while node.right != None: # While there is still a value to the right tree
			node = node.right # Grab next node
		return node.value # Return max value found

	def min(self):
		node = self.root # Grab the root
		while node.left != None: # While there is still a value to the left of the tree
			node = node.left # Grab next node
		return node.value # Return minimum value found

	def predicesor(self, value):
		node = self.search(value)
		if node == None: # If the root is the value of interest
			return None # Return None as no predicesor is possible
		if node.left != None: # If their is a left subtree
			node = node.left # Iterate through left subtree till you find the largest value
			while node.right != None:
				node = node.right
			return node
		else: # If their isn't a left subtree
			while node.parent.value > value:
				node = node.parent
				if node.parent == None:
					return None
			return node.parent


	def successors(self, value):
		node = self.root # Grab the node of interest
		while node != None and node.value != value: # While the node found is not none and isn't the value of interest
			if node.left.value > value: # Move left if the left child is bigger
				node = node.left
			else: # Mode right if not
				node = node.right
		return node # Return node with children

	def traverse(self, tree = None): # In-order traversal
		if tree == None:
			tree = self.root
		if tree.left != None:
			self.traverse(tree.left)
		print(tree.value)
		if tree.right != None:
			self.traverse(tree.right)
		return tree.value

	def delete(self, value = None, node = None): # O(Height)
		if node == None: node = self.search(value)
		if value == None: value = node.value
		children = []
		if node.left != None: children.append(node.left)
		if node.right != None: children.append(node.right)
		print(f"Deleting node {node.value} with {len(children)} children")
		if len(children) == 0: # If no children depend on node
			parent = node.parent
			if parent.left != None and parent.left.value == value:
				parent.left = None # simply delete node
			else:
				parent.right = None
		if len(children) == 1: # If node has one child, splice the value out
			parent = node.parent
			if parent.left != None and parent.left.value == value:
				parent.left = children[1]
			else:
				parent.right = children[0]
		if len(children) == 2:
			predicesor_node = self.predicesor(value)
			if predicesor_node != None:
				node.value, predicesor_node.value = predicesor_node.value, node.value
				self.delete(node = predicesor_node) # Call delete recursively now that value is in an easily deletable position
			else:
				print(f"Deletion operation failed on node of value {value} with {len(children)} children")

	def select(self, order):
		node = self.root
		current_order = 0
		while node.left != None and node.left.size() > order:
			node = node.left
			current_order = node.left.size()
		while current_order != order:
			current_order -= node.left.size()
			order -= node.left.size() + 1
			node = node.right
		return node.value

	def rank(self, value):
		node = self.root
		current_rank = 0
		while node != None and node.value != value:
			if node.value < value:
				if node.left != None:
					current_rank += node.left.size()
				current_rank += 1
				node = node.right
			if node.value > value:
				node = node.left
			if node == None: # if the new node does not have a value
				return None # Return that the value was not found in the tree
		if node.left != None:
			current_rank += node.left.size()
		return current_rank

	def rotate_left(self, child):
		parent = child.parent
		A = parent.left
		B = child.left
		C = child.right
		parents_parent = parent.parent
		if parents_parent == None: # If the parent is the root
			self.root = child
		elif parents_parent.left == parent:
			parents_parent.left = child
		else:
			parents_parent.right = child
		child.left = parent
		child.right = C
		parent.left = A
		parent.right = B
		return

	def rotate_right(self, child):
		parent = child.parent
		A = parent.right
		B = child.left
		C = child.right
		parents_parent = parent.parent
		if parents_parent == None:
			self.root = child
		elif parents_parent.left == parent:
			parents_parent.left = child
		else:
			parents_parent.right = child
		child.right = parent
		child.left = A
		parent.left = B
		parent.right = C
		return

class Node:
	def __init__(self, parent, value):
		self.parent = parent # Need parent for finding predicesor and also inevitably deleting values
		self.value = value
		self.left = None
		self.right = None


	def __repr__(self):
		return f"Node Value: {self.value}"

	def size(self):
		size = 1
		if self.left != None:
			size += self.left.size()
		if self.right != None:
			size += self.right.size()
		return size


# ------------------------ Heap Data Structure ------------------------ #
# This data structure is used to easily find the minimum/maximum if
# if you find yourself constantly calculating the minimum of a list.
# The last class generates and maintains two heaps (one min and one max)
# allowing for the median to quickly be found at any given moment
class MinHeap:
	def __init__(self, content = None):
		self.heap = []
		if content == None:
			content = random.sample(range(1, 10), 8)
		self.batch_insert(content)

	def __repr__(self):
		return f"Heap: {self.heap}"

	def insert(self, value):
		self.heap.append(value)
		value_position = len(self.heap)
		if len(self.heap) == 1: return
		while self.heap[(value_position >> 1) - 1] > value and value_position > 1:# Bubble-up while parent is larger
			self.heap[value_position - 1], self.heap[(value_position >> 1) - 1] = self.heap[(value_position >> 1) - 1], self.heap[value_position - 1]# Swap child and parent if necessary
			value_position = value_position >> 1 # Correct the value position

	def batch_insert(self, values):
		for value in values:
			self.insert(value)

	def extract_min(self): # Function probably has high constant and could be simplified
		if len(self.heap) == 0: return None
		self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]# Switch the first and last positions - Preserves structure
		min = self.heap.pop() # Pop mininimum value now at the end of the heap
		if len(self.heap) == 0: return min # If the heap is empty, return minimum
		value = self.heap[0] # Set value violating heap property as the first value
		position = 1 # Set position of value violating heap property
		while (position << 1) <= len(self.heap): # While value violating heap properity has children
			first_child = self.heap[(position << 1) - 1] # Grab the first child
			if (position << 1) < len(self.heap): second_child = self.heap[(position << 1)] # If there is a second child grab it
			else: second_child = float('inf') # Else declare the second child as infinity
			#print(f"{position} --> {position << 1} - {first_child} brother of {second_child} - {value} value")
			if first_child >= value and second_child >= value: break # If the heap property has been restored break loop
			if first_child <= second_child and first_child < value: # If first child is bigger than second child and larger than the value of interest
				self.heap[(position << 1) - 1], self.heap[position - 1] = self.heap[position - 1], self.heap[(position << 1) - 1] # Swap value of interest and first child
				position = (position << 1) # Srt new position of value of interest
			if first_child > second_child and second_child < value: # If second child is larger and the value is larger than the value of interest
				self.heap[(position << 1)], self.heap[position - 1] = self.heap[position - 1], self.heap[(position << 1)] # Swap value of interest and second child
				position = (position << 1) + 1 # Set new position of value of interest
		return min

	def find_min(self):
		return self.heap[0]

	def size(self):
		return len(self.heap)

class MaxHeap:
	def __init__(self, content = None):
		self.heap = []
		if content == None:
			content = random.sample(range(1, 10), 8)
		self.batch_insert(content)

	def __repr__(self):
		return f"Heap: {self.heap}"

	def insert(self, value):
		self.heap.append(value)
		value_position = len(self.heap)
		if len(self.heap) == 1: return # If the heap only has a single value in it
		while self.heap[(value_position >> 1) - 1] < value and value_position > 1:# Bubble-up while parent is larger
			self.heap[value_position - 1], self.heap[(value_position >> 1) - 1] = self.heap[(value_position >> 1) - 1], self.heap[value_position - 1]# Swap child and parent if necessary
			value_position = value_position >> 1 # Correct the value position

	def batch_insert(self, values):
		for value in values:
			self.insert(value)

	def extract_max(self): # Function has high constant and could be simplified
		if len(self.heap) == 0: return None
		self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]# Switch the first and last positions - Preserves structure
		max = self.heap.pop() # Pop mininimum value now at the end of the heap
		if len(self.heap) == 0: return max # If the heap is empty, return minimum
		value = self.heap[0] # Set value violating heap property as the first value
		position = 1 # Set position of value violating heap property
		while (position << 1) <= len(self.heap): # While value violating heap properity has children
			first_child = self.heap[(position << 1) - 1] # Grab the first child
			if (position << 1) < len(self.heap): second_child = self.heap[(position << 1)] # If there is a second child grab it
			else: second_child = float('-inf') # Else declare the second child as negative infinity
			if first_child <= value and second_child <= value: break # If the heap property has been restored break loop
			#print(f"First Child {first_child} - Second Child {second_child} - Value {value}")
			if first_child >= second_child and first_child > value: # If first child is bigger than second child and larger than the value of interest
				self.heap[(position << 1) - 1], self.heap[position - 1] = self.heap[position - 1], self.heap[(position << 1) - 1] # Swap value of interest and first child
				position = (position << 1) # Srt new position of value of interest
			if first_child < second_child and second_child > value: # If second child is larger and the value is larger than the value of interest
				self.heap[(position << 1)], self.heap[position - 1] = self.heap[position - 1], self.heap[(position << 1)] # Swap value of interest and second child
				position = (position << 1) + 1 # Set new position of value of interest
		return max

	def find_max(self):
		return self.heap[0]

	def size(self):
		return len(self.heap)

class MedianMaintainer:
	def __init__(self, content = None):
		self.UH = MinHeap(content = []) # Initialize an empty min heap as the upper heap
		self.LH = MaxHeap(content = []) # Initialize an empty max heap as the lower heap
		if content == None: # If no content passed
			content = random.sample(range(1, 10), 8) # Generate a random sample
		self.median = 0
		self.median_sum = 0
		self.batch_insert(content)

	def __repr__(self):
		return f"Lower Heap: {self.LH.heap}\nUpper Heap: {self.UH.heap}"


	def insert(self, value):
		if value < self.median:
			self.LH.insert(value)
		else:
			self.UH.insert(value)
		if abs(self.LH.size() - self.UH.size()) > 1:
			self.rebalance()
		self.median = self.find_median()
		self.median_sum += self.median
		return

	def batch_insert(self, contents):
		for value in contents:
			self.insert(value)
			self.__repr__

	def rebalance(self):
		if self.LH.size() > self.UH.size():
			self.UH.insert(self.LH.extract_max())
		else:
			self.LH.insert(self.UH.extract_min())

	def find_median(self):
		if self.UH.size() > self.LH.size(): # If the upper heap is bigger or equal to the lower heap size
			return self.UH.find_min() # Grab min value in upper heap
		else: # If the lower heap is bigger in size of the upper heap
			return self.LH.find_max() # Grab max value in lower heap



def load_assignment():
	f = open('median.txt', 'r')
	data = f.read().split('\n')
	data.pop()
	data = [int(datum) for datum in data]
	return data

# ----------------- Excess Functions ----------------- #

def random_ip():
	IP = ''
	for f_ind in range(4):
		for s_ind in range(4):
			IP += str(random.randint(0, 9))
		if f_ind < 3:
			IP += '.'
	return IP

def find_primes(start = 1, end = 100):
	primes = []
	for x in range(100):
		if x <= 1: continue
		for i in range(2, x):
			if x%i == 0:
				break
		else: primes.append(x)
	return primes

def next_prime(start):
	for x in range(start, start + 1000):
		if x <= 1: continue
		for i in range(2, start):
			if x%i == 0:
				break
		else: return x
	return None

def to_bytes(string, encoding = 'utf-8'):
	return sum(bytes(string, encoding))

def split(key):
	return [char for char in key]


def load_twosum_assignment(sort = True):
	contents = open('2sum-prob.txt', 'r').read()
	data = contents.split('\n')
	data.pop()
	data = [int(datum) for datum in data]
	if sort == True: data.sort()
	return data

def assess_twosums_heaps(data = None, lower_bound = -10000, upper_bound = 10000):
	# Working function to assess for pairs of numbers within a list that add up to t within a range
	# Seems to run quickly and theoretically runs in O(n) with a O(n + t) space complexity,
	# however the algorithms seems to have high constants and could be simplified
	if data == None:
		start = time.time()
		data = load_twosum_assignment()
		load_time = (time.time() - start)
	else:
		load_time = "N/A"

	middle = int(len(data)/2)

	start = time.time()
	minheap = MinHeap(data[:middle])
	min = minheap.extract_min()

	maxheap = MaxHeap(data[(middle - 1):])
	max = maxheap.extract_max()
	heapify_time = (time.time() - start)


	t_dic = {point: True for point in range(-10000, 10000)}

	print(f'Data Loaded ({round(load_time, 5)} sec) and Heapified ({round(heapify_time, 5)} sec)... Running Assessment')

	start = time.time()
	distinct_pairs = 0
	while max != None and min != None:
		#print(f'Heap Length - {str(len(maxheap.heap))} - Min of {min} - Max of {max} - T of {max + min}')
		if min == max: break
		t = max + min
		if t < lower_bound:
			min = minheap.extract_min()
		elif t > upper_bound:
			max = maxheap.extract_max()
		else:
			if t_dic[t] == True:
				distinct_pairs += 1
				t_dic[t] = False
				#print(f"Distinct pair ({max}, {min}) found adding to {t}")
			min = minheap.extract_min()
			if max + min > upper_bound:
				minheap.insert(min)
				max = maxheap.extract_max()
	runtime = (time.time() - start)
	print(f"2-Sum Script Complete - {distinct_pairs} Distinct Pairs Found ({round(runtime, 5)} sec)")

def assess_twosums_tree(data = None, lower_bound = -10000, upper_bound = 10000):
	if data == None:
		start = time.time()
		data = load_twosum_assignment(sort = False) # Load data without sorting to avoid tall binary tree
		load_time = (time.time() - start)
	else:
		load_time = "N/A"

	start = time.time()
	tree = BinaryTree(data) #
	binarizing_time = (time.time() - start)

	t_uht = UniversalHashTable(data = range(-10000, 10001))
	root = tree.root
	smaller_branch = root.left
	bigger_branch = root.left

	while smaller_branch != None and bigger_branch != None:
		t = bigger_branch.value + smaller_branch.value
		if t < lower_bound: # Grab a bigger branch
			bigger_branch = bigger_branch.right
		elif t > upper_bound: # Grab a smaller branch
			smaller_branch = smaller_branch.left
		else:

	return
