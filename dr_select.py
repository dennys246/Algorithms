import time, math, random
import matplotlib.pyplot as plt

class Selector:

	def __init__(self):
		self.min = 1
		self.max = 101
		self.size = 100

	def run(self):
		array = self.new_list()
		if len(array) % 2 == 0:
			order_statistic = int(len(array)/2)
		else:
			order_statistic = int((len(array) + 1)/2)

		earlier = time.time()
		selection = self.rselect(array[:], order_statistic)
		later = time.time()
		speed = (later - earlier)
		print(f"Rselects speed of {speed} seconds")

		earlier = time.time()
		subarray, dselection = self.dselect(array[:], order_statistic)
		later = time.time()
		speed = (later - earlier)
		print(f"Dselects speed of {speed} seconds")

		print(f"subarray --> {subarray} --> {dselection}\nRselect --> {selection}")

		if subarray[dselection] == selection:
			print("Search failed!")

		earlier = time.time()
		sorted_array = self.quicksort(array[:])
		later = time.time()
		speed = (later - earlier)
		print(f"Quicksort speed of {speed} seconds")

	def plot(self):
		min_value = 100000
		max_value = 10000000
		step = 100000
		list_sizes = range(min_value, max_value, step)
		rselect_speeds = []
		dselect_speeds

		for size in list_sizes:
			array = self.new_list(size)
			if size % 2 == 0:
				os = int(size/2)
			else:
				os = int((size + 1)/2)

			earlier = time.time()
			rselection = self.rselect(array[:], os)
			later = time.time()
			rselect_speeds.append((later - earlier))

			earlier = time.time()
			subarray, dselection = self.dselect(array[:], os)
			later = time.time()
			dselect_speeds.append((later - earlier))

		self.plot_timings(rselect_speeds, dselect_speeds, list_sizes)

	def plot_timings(self, rselect_speeds, dselect_speeds, list_sizes):
		plt.plot(list_sizes, rselect_speeds, label = "RSelect Speeds")
		plt.plot(list_sizes, dselect_speeds, label = "DSelect Speeds")
		plt.xlabel("List Size")
		plt.ylabel("RSelect Time (Seconds)")
		plt.title("RSelect Timings over List Size")
		plt.legend()
		plt.show()
		plt.close()
		return

	def rselect(self, array, order_statistic):
		if len(array) == 1:
			return array[0]

		pivot_ind = random.randint(0, len(array) - 1)

		if pivot_ind != 0:
			array[0], array[pivot_ind] = array[pivot_ind], array[0]
		i = 1
		pivot = array[0]
		for j in range(1, len(array)):
			if array[j] < pivot:
				array[j], array[i] = array[i], array[j]
				i += 1

		if i == order_statistic:
			return array[0]

		array[0], array[i - 1] = array[i - 1], array[0]
		if i > order_statistic:
			return self.rselect(array[:(i - 1)], order_statistic)
		else:
			return self.rselect(array[i:], order_statistic - i)

	def dselect(self, array, order_statistic):
		# Note this function is not better practically than rselect as it has a higher coefficient
		# and uses more memory slowing down the algorithm. That being said it is more stable
		# and will never have quadratic running time
		if len(array) <= 5:
			array = self.quicksort(array)
			return array, len(array) >> 1

		n = len(array)

		# ---- Median of medians! ---- #
		array = [self.quicksort(array[x:(x + 5)]) for x in range(0, n - 5, 5)] # Break A into groups of 5
		array = [subarray[len(subarray) >> 1] for subarray in array]
		print(array)
		array, pivot_ind = self.dselect(array, round(n/10))
		# ---------------------------- #

		if pivot_ind != 0:
			array[0], array[pivot_ind] = array[pivot_ind], array[0]
		i = 1
		pivot = array[0]
		for j in range(1, len(array)):
			if array[j] < pivot:
				array[j], array[i] = array[i], array[j]
				i += 1

		if i == order_statistic:
			return array, 0

		array[0], array[i - 1] = array[i - 1], array[0]
		if i > order_statistic:
			return self.dselect(array[:(i - 1)], order_statistic)
		else:
			return self.dselect(array[i:], order_statistic - i)


	def new_list(self, size = None):
		if size == None:
			size = self.size
		return random.sample(range(self.min, self.max), size)


	def quicksort(self, array = None):
		if array is None:
			array = self.list
		if len(array) <= 1:
			return array
		i = j = 1
		pivot_ind = random.randint(0, len(array) - 1)
		if pivot_ind != 0:
			array[0], array[pivot_ind] = array[pivot_ind], array[0]
		pivot = array[0]
		while j < len(array):
			if array[j] < pivot:
				array[j], array[i] = array[i], array[j]
				i += 1
			j += 1
		array[0], array[i - 1] = array[i - 1], array[0]
		array[:(i - 1)] = self.quicksort(array[:(i - 1)])
		array[i:] = self.quicksort(array[i:])
		return array
